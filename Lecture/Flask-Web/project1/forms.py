from . import bcrypt
from .models import Users
from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
                    TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email,\
                    EqualTo, ValidationError,Optional


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),
                            Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password')])
    submit_field = SubmitField('Sign Up')

    @property
    def hashed_password(self):
        try:
            password = self.password.data.strip()
            return bcrypt.generate_password_hash(password).decode('utf-8')
        except:
            pass

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError( '''That username is taken.
                                    Please choose a different one.'''
                                  )

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError( '''That email is taken.
                                     Please choose a different one.'''
                                  )


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit_field = SubmitField('Login')

    def password_is_validate(self,password):
        if bcrypt.check_password_hash(password.strip(),self.password.data):
            return True



class SearchForm(FlaskForm):
    radio = RadioField('Select',
                        default="title",
                        choices=[('title','title'),('author','author'),
                            ('year','year'),('isbn','isbn')],
                        validators=[DataRequired()]
                        )
    search = StringField('Search',validators=[DataRequired()])
    submit_field = SubmitField('Search')


class ReviewForm(FlaskForm):
    textfield = TextAreaField('Write a review', 
            #render_kw=dict(rows=8,cols=45),
            validators=[DataRequired('Review can not be empty'),
                        Length(max=500)])

    ratefield = RadioField('Rate',
                    #default="5 stars",
                    choices=[('one','1 &#11088; '),('two','2 &#11088; '),
                        ('three',' 3 &#11088; '),('four','4 &#11088; '),('five','5 &#11088;') ],
                    validators=[DataRequired()]
                    )

    submit_form = SubmitField('Submit Form')

    def validate_textfield(self, text):
        print('\n\nVAL_TEXT:',text)
        if not text:
            raise ValidationError( '''No character enter !!''')

    def validate_ratefield(self, text):
        if not text:
            raise ValidationError( '''please select a rate !!''')


