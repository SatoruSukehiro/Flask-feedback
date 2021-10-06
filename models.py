"""basic database setup and connection to app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref




db = SQLAlchemy()
def connect_db(app):
    '''connects database'''
    db.app=app
    db.init_app(app)



bcrypt = Bcrypt()
class User(db.Model):
    """creates users table"""
    __tablename__ = "users"
    username = db.Column(db.String(20),
                         primary_key=True)

    password = db.Column(db.String,
                         nullable=False)

    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)
    feedback = db.relationship("Feedback",cascade="all,delete",backref='user')

    @classmethod
    def register(cls,username,password,email,first_name,last_name):
        password= bcrypt.generate_password_hash(password)
        utf8_hashed = password.decode('utf8')
        return cls(username=username,password=utf8_hashed, first_name=first_name,last_name=last_name,email=email)

    @classmethod
    def verify(cls,username,password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            return user
        else:
            return False

 
            
    def __repr__(self):
        return f"<username:{self.username} password:{self.password} email:{self.email} name: {self.first_name} feedback:{self.feedback} last name: {self.last_name}>"


class Feedback(db.Model):
    """Creates feedback table"""
    __tablename__ = 'feedback'
    id = db.Column(db.Integer,primary_key=True,
                                autoincrement=True)
    
    title = db.Column(db.String(100),nullable=False)

    content= db.Column(db.String,nullable=False)

    username = db.Column(db.String,db.ForeignKey('users.username'),nullable=False)











