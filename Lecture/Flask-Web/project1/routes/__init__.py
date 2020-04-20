import re
from .. import app, db
from ..models import *
from flask import render_template,\
                  url_for, redirect,flash,\
                  request, jsonify

from flask_login import login_user, logout_user,\
                        login_required, current_user

from sqlalchemy.exc import OperationalError


@app.errorhandler(404)
def handle_error(error):
    message = "Please check url path and try again.."
    status_code = 500
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }
    return jsonify(response), status_code

@app.errorhandler(OperationalError)
def ServerClosedError():
    return render_template('error.html',error=4)

