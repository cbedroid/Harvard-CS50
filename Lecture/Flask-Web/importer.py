""" 
    In this file, I will collect all data from 'books.csv'
    and insert each row into the corresponding Heroku table.
"""
import csv
from project1 import app,db
from project1.models import *
from booksetup import GoodRead 

class Book(Books):
    all_authors  = {}
    all_years = {}

    def __init__(self,isbn,title,cover_image):
        self.isbn = isbn
        self.title = title 
        self.cover_image = cover_image
        
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

        

def writeDatabase():
    # Here we will create each book's column.
    all_authors = []
    all_years = []
    
    GR = GoodRead()
    books = GR.readCsv()
    isbns = [x[0] for x in books]
    GR.run()
    images = GR.images # books cover images

    if not images:
        raise TypeError('NO IMAGES')
    count = 0
    for isbn,title,author,year in books:
        book = Book(isbn,title,cover_image=images[count])
        book.add_author(Creator(author))
        book.add_publish(PublishDate(year))
        db.session.add(book)
        count+=1
    db.session.commit()
    print('Books added: successfully')


if __name__ == "__main__":
    with app.app_context():
        main()

