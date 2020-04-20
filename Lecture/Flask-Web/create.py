""" 
    This file will establish connection to Heroku database.
    Once Intialized,  all  table's name,rows and column will be popluated
    inside each of the Herouke databases.
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

