from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate

#Inintializing SqlAlchemy
#Used to cetae database



db = SQLAlchemy()

'''
UserMixin is a helper class from Flask-Login that provides default implementations for 
certain user authentication methods. This allows your User model to work seamlessly with 
Flask-Login for user authentication and session management.

'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), unique=True, nullable=False)

    lastname = db.Column(db.String(50), unique=True, nullable=False)
    
    username = db.Column(db.String(50), unique=True, nullable=False)
    
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    stats = db.relationship('UserStats', backref='user', uselist=False)  # One-to-One Relationship

class UserStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    games_played = db.Column(db.Integer, default=0)
    best_score = db.Column(db.Integer, default=0)
    total_wins = db.Column(db.Integer, default=0 , nullable=True )  # Number of games won
    total_attempts = db.Column(db.Integer, default=0  ,nullable=True) 

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    difficulty = db.Column(db.String(10))
    number_to_guess = db.Column(db.Integer)
    attempts_left = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
