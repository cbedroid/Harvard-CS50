from . import bcrypt
from .models import Users
from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
                    TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email,\
                    EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),
                            Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password')])
    submit_field = SubmitField('Sign Up')

    @property
    def hashed_password(self):
        try:
            return bcrypt.generate_password_hash(self.password.data).decode('utf-8')
        except:
            pass

    def validateUser(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validateEmail(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit_field = SubmitField('Login')

    def password_is_validate(self,password):
        if bcrypt.check_password_hash(password,self.password.data):
            return True

class RadioForm(FlaskForm):
    radio = RadioField('Select',
                        default="title",
                        choices=[('title','title'),('author','author'),
                            ('year','year'),('isbn','isbn')],
                        validators=[DataRequired()]
                        )


class InputForm(FlaskForm):
    search = StringField('Search',validators=[DataRequired()])
    submit_field = SubmitField('Search')

                                        

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),
                               Length(min=2, max=20)])
    email = StringField('Email',
                               validators=[DataRequired(), Email()])

    submit_field = SubmitField('Update')

    def validateUser(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validateEmail(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit_field = SubmitField('Request Password Reset')

    def validateEmail(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit_field = SubmitField('Reset Password')
