from . import *
from ..forms import RegistrationForm, LoginForm
from sqlalchemy.exc import OperationalError

@app.route('/login',methods=['GET','POST'])
def login():

    previous_page = request.args.get('next')
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
            if previous_page:
                return redirect(previous_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Sorry, Login was unsuccessful! Please check username or password!','danger') 
    return render_template('login_register.html',title='Login',form=login,isLoginForm=True)


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
        firstname = registration.firstname.data
        lastname = registration.lastname.data
        password = registration.hashed_password #encrypting password

        #Creating user 
        user = Users(username=username,firstname=firstname,
                    lastname=lastname,email=email,password=password)
        db.session.add(user)
        db.session.commit()

        flash('Your account was created successfully','success')
        return redirect(url_for('login'))
    return render_template('login_register.html',title="Register",form=registration,isLoginForm=False)


