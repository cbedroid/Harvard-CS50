""" 
This file will handle rendering an error template 
when user tries to access sensitive data while not logged in.
Also this BaseRedirect will redirect any routes where its return
value is `None` or its return value DOES NOT render a template.
( `None` types from sqlalchemy query will be consider a None value )   
""" 

from functools import wraps
from flask import render_template, url_for, redirect,request

def BaseRedirect(user=None):
    """ Redirect non-authenticated user to error page"""
    def outer(f):
        @wraps(f)
        def inner(*args,**kwargs):
            if not user.is_authenticated:
                return redirect(url_for('login',next='search'))
            
            returned_results = f(*args,**kwargs)
            error_msg = {}
            if not returned_results:
                if kwargs:
                    error_msg = dict(reason=kwargs.get('search',None),
                                     category=kwargs.get('searchby',None)
                                     )
                return render_template('error.html',error=2,error_msg=error_msg)
            return returned_results
        return inner
    return outer


# login required function, yes I know I could have used it instead
redirectUnauthorizedUser = BaseRedirect 

# redirect any pages the does not render or redirect to a template
# also catch error in routes 
redirectOnNone = BaseRedirect

