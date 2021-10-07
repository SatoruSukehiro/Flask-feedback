from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired,Length,Email



class RegisterUser(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=1,max=20)])

    password=  PasswordField('Password',validators=[DataRequired()])

    email= StringField('Email',validators=[DataRequired()])

    first_name= StringField("First Name",validators=[DataRequired()])

    last_name=  StringField("Last Name",validators=[DataRequired()])  


class Login(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=1,max=20)])

    password= PasswordField('Password',validators=[DataRequired()])


class FeedbackForm(FlaskForm):
    title = StringField('Title', validators= [DataRequired()])
    
    content = TextAreaField('Content',validators=[DataRequired()])