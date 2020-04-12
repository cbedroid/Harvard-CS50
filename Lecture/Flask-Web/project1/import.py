""" 
    In this file, I will collect all data from 'books.csv'
    and insert each row into the corresponding Heroku table.
"""
import os
import csv
from . import app,db
from .models import *


class Setup():
    @staticmethod
    def getBooks():
        # open book.csv
        with  open('books.csv') as f:
            return  list(csv.reader(f,delimiter=','))

    @staticmethod
    def filterAuthors(author):
        """Remove duplicant rows from csv author list"""
        return set(author)

    @staticmethod
    def filterYears(years):
        """Remove duplicant rows from csv years list"""
        return set(author)


class Book(Books):
    all_authors  = {}
    all_years = {}

    def __init__(self,isbn,title):
        self.isbn = isbn
        self.title = title 
        
    def add_author(self,creator):
        author = creator.name
        if author not in self.all_authors:
            self.author_id = creator.id
            self.all_authors[author] = self.author_id
            db.session.add(creator)
        else:
            self.author_id = self.all_authors[author]

    def add_publish(self,publish):
        year = publish.year
        if year not in self.all_years:
            self.publish_id = publish.id
            self.all_years[year] = self.publish_id
            db.session.add(publish)
        else:
            self.publish_id = self.all_years[year]


class Creator(Authors):
    index = 1
    def __init__(self,name):
        self.id = self.index
        self.name = name 
        Creator.index+=1


class PublishDate(Publish):
    index = 1
    def __init__(self,year):
        self.year = year
        self.id = self.index
        PublishDate.index+=1

        

def main():
    # Here we will create each book's column.
    all_authors = []
    all_years = []
    
    for isbn,title,author,year in Setup.getBooks():
        book = Book(isbn,title)
        book.add_author(Creator(author))
        book.add_publish(PublishDate(year))
        db.session.add(book)
        #print(f'Added {author} Book {title}')
    db.session.commit()
    print('Books added: successfully')


if __name__ == "__main__":
    with app.app_context():
        main()

