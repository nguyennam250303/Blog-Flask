from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import data_required, Length, EqualTo, ValidationError
from flaskblog.models import User


class LoginForm(FlaskForm):
    username = StringField(label="Username :", validators=[data_required(),Length(min = 6, max = 50)])
    password = PasswordField(label = "Password :", validators=[data_required(),Length(min = 6, max = 30)])
    submit = SubmitField(label = "Login")


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        if User.query.filter_by(username=username_to_check.data).first():
            raise ValidationError("Username have exists, Please type another username")

    def validate_email_address(self, email_address_to_check):
        if User.query.filter_by(email_address=email_address_to_check.data).first():
            raise ValidationError("Email address have exists, Please type another Email address")

    username = StringField(label="Username :", validators=[data_required(),Length(min = 6, max = 50)])
    email_address = EmailField(label = "Email Adrress :", validators=[data_required()])
    password1 = PasswordField(label = "Confirm Password :", validators=[data_required(),Length(min = 6, max = 30)])
    password2 = PasswordField(label="Password :", validators=[EqualTo('password1')])
    submit = SubmitField(label = "Register")


class ViewPost(FlaskForm):
    submit = SubmitField(label = "Detailed View")

class CreatePostForm(FlaskForm):
    name_post = StringField(label="Name Post :", validators=[data_required(), Length(min=1, max=30)])
    body = TextAreaField(label="Content :",validators=[data_required()])

    submit =SubmitField(label="Create")
