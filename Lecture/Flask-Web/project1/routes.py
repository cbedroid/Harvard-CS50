import os
from . import app, db 
from .models import *
from functools import wraps
from .api import GoodReads
from .forms import RegistrationForm, LoginForm,RadioForm,InputForm
from flask import render_template,\
                  url_for, redirect,flash,\
                  request, jsonify
from flask_login import login_user, logout_user,\
                        login_required, current_user


def redirectNonUser(errorcode=1):
    """ Redirect non-authenticated user to error page"""
    def outer(f):
        @wraps(f)
        def inner(*args,**kwargs):
            if not current_user.is_authenticated:
                return render_template('error.html',error=errorcode)
            return f(*args,**kwargs)
        return inner
    return outer


@app.route("/",methods=['GET'])
@app.route("/home",methods=['GET'])
def home():
    
    data = GoodReads.readXml('sample.xml')
    return render_template('index.html',title="JustBookItUp",
            books=data)



@app.route("/search",methods=['GET','POST'])
@redirectNonUser(1)
def search():

    radioform = RadioForm()
    textform = InputForm()

    radio = radioform.radio.data
    search = textform.search.data

    if request.method.lower() == 'post':
        # check whether user fill out both froms: radio and search fields
        # radio form default value ='title' 
        # so we will just check the value of `search`
        if search:
            return redirect(url_for('searchFor',radio=radio,search=search,page=1))

        else:
            # Flash error message when search field was not entered
            flash('You must enter either a book, author, isbn, or year','danger')
            return redirect(url_for('search'))
        
    return render_template('search.html',radioform=radioform,textform=textform)

    
@app.route('/api/search/<string:radio>/<string:search>/<int:page>',methods=['GET','POST'])
@redirectNonUser(1)
def searchFor(radio,search,page=1):
    
    data = {'total':0, 'results':None}
    if radio == "title":
        search = search.strip()
        results = Books.query.filter(Books.title.like(f'%{search}%'))
        data.update(results=results.paginate(per_page=25,page=page))

    total = data['results'].total or 0
    data.update(total=total)
    return render_template('books.html',search=search,radio=radio,data=data)


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated: # User is already logged in  
        return redirect(url_for('home'))

    login = LoginForm()
    if login.validate_on_submit():

        # Get the first account with the matching email address
        email_address = login.email.data
        user = Users.query.filter_by(email=email_address).first()
        rememberme = login.remember.data

        # Check for password
        # because the password has sensitive information, we should
        # let a function handle the conversion ,instead of capturing it into a variable

        if user and login.password_is_validate(user.password):
            # Begin the user session
            login_user(user)
            endpoint = request.args.get('next')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!','danger') 
    return render_template('user.html',title='Login',form=login,isLoginForm=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated: # User is already logged in  
        return redirect(url_for('home'))

    registration = RegistrationForm()
    if registration.validate_on_submit():
        username = registration.username.data
        email = registration.email.data
        password = registration.hashed_password #encrypting password
        if not password:
            print('Error: password was not enter')
            return 'Error'  #TODO: redirect to error page here
        
        #Creating user 
        user = Users(username=username,email=email,password=password)
        db.session.add(user)
        db.session.commit()

        flash('Your account was created successfully')
        return redirect(url_for('login'))
    return render_template('user.html',title="Register",form=registration,isLoginForm=False)



