""" 
    This file will establish connection to Heroku database
    and the creation of the tables inside each of the  databases.
"""

import os 
from flask import Flask
from .models import *
from . import app,db



def main():
    # Create tables
    print('Initializing...')
    db.create_all()


if __name__ == '__main__':
    with app.app_context():
        main()
        print('Completed')

