from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import random
from flask_bcrypt import Bcrypt

#To hash password
from werkzeug.security import generate_password_hash, check_password_hash
#For Creating and Adding all the data to the database
from flask_migrate import Migrate
import random
import math
from models import db, User, UserStats, GameSession, Feedback 


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


# Initialize Flask-Migrate

from models import User,db
db.init_app(app)
migrate = Migrate(app, db)


#bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#Login route
@app.route("/login",methods=["POST","GET"])
def login():
    
 if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'{current_user.username}  logged in successfully!!!!','success')
            return redirect(url_for("welcome"))
        else:
            flash("Invalid credentials. Try again.",'danger')
 return render_template("login.html")




# Register route
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if password == password2:
            generate_password = generate_password_hash(password, method="pbkdf2:sha256")

            try:
                new_user = User(
                    username=username,
                    password=generate_password,
                    firstname=firstname,
                    lastname=lastname,
                    email=email
                )
                db.session.add(new_user)
                db.session.commit()
                flash("User Registered Successfully!", "success")
                return redirect(url_for("login"))

            except Exception as e:
                db.session.rollback()  # Rollback if an error occurs
                flash(f"Error: {str(e)}", "danger")

            finally:
                db.session.close()  # Closing session properly

        else:
            flash("Passwords do not match!", "danger")
        
    return render_template("register.html")



#Logout Route

@app.route("/logout")
def logout():

    logout_user()
    flash("User has been logged out!!",'success')
    return redirect(url_for("login"))


#Main page route
@app.route("/", methods=['POST', 'GET'])
@login_required
def index():
    message = ""  
    username = current_user.username  

    # Ensure user stats exist
    user_stats = UserStats.query.filter_by(user_id=current_user.id).first()
    if not user_stats:
        user_stats = UserStats(user_id=current_user.id, games_played=0, best_score=0, total_wins=0, total_attempts=0)
        db.session.add(user_stats)
        db.session.commit()
        db.session.close()
                

    # Initialize game session
    if "random_number" not in session:
        session["random_number"] = random.randint(1, 10)

        session["attempts"] = 0  

    if request.method == "POST":
        user_guess = request.form.get("guess")

        if user_guess:
            try:
                user_guess = int(user_guess)
                session["attempts"] += 1  

                if user_guess == session["random_number"]:
                    message = f" Correct! You guessed in {session['attempts']} attempts!"

                    # 🟢 **Accumulate New Attempts & Score in the Database**
                    user_stats.games_played += 1
                    user_stats.total_wins += 1

                    #  Add new attempts to total attempts

                    user_stats.total_attempts += session["attempts"]  

                    #  Increase total score (assuming each win gives +5 points)
                    new_score = 5  
                    user_stats.best_score += new_score  

                    # 🟢 Update best score if it's the lowest attempt game
                    if user_stats.best_score == 0 or session["attempts"] < user_stats.best_score:
                        user_stats.best_score = session["attempts"]

                    
                    db.session.commit()
                    db.session.close()
                

                    # Reset game session
                    session.pop("random_number")
                    session.pop("attempts")

                elif user_guess > session["random_number"]:
                    message = "Too high! Try again."
                else:
                    message = "Too low! Try again."

            except ValueError:
                message = "Please enter a valid number!"

    return render_template("home.html", message=message, username=username)


@app.route("/welcome")
@login_required
def welcome():

    return render_template('welcome.html')



@app.route("/leaderboard")
@login_required
def leaderboard():
    # Fetch all users' stats and sort by total_wins (highest) and total_attempts (lowest)
    leaderboard_data = UserStats.query.order_by(UserStats.total_wins.desc(), UserStats.total_attempts.asc()).all()

    return render_template("leaderboard.html", leaderboard=leaderboard_data)


@app.route("/contact")
def contact():

    return render_template('contact.html')

@app.route("/profile")
def profile():

    user_data_game = UserStats.query.filter_by(user_id=current_user.id).first()
    user_data =User.query.filter_by(id=current_user.id).first()

    return render_template('profile.html',user_data_game=user_data_game,user_data= user_data)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the database file if not exists

    app.run(debug=True)



# matin
#1234



'''
TBOIII
123
'''