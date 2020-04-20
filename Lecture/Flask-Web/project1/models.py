from .  import db,login_manager,app
from .api import GoodReads
from flask_login import UserMixin
from sqlalchemy import *
#from .testsort import Sorter



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model,UserMixin):
    __tablename = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,nullable=False,unique=True)
    username = db.Column(db.String,nullable=False,unique=True)
    firstname = db.Column(db.String,nullable=True)
    lastname = db.Column(db.String,nullable=True)
    password = db.Column(db.String,nullable=False)


class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer,primary_key=True)
    reviews = db.Column(db.String, nullable=False)
    book_id = db.Column(db.Integer,db.ForeignKey('books.id'),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    books = db.relationship('Books',backref='reviews',lazy=True)
    user = db.relationship('Users',backref='reviews',lazy=True)


class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer,primary_key=True)
    isbn = db.Column(db.String,nullable=False,unique=True)
    title = db.Column(db.String, nullable=False)
    cover_image = db.Column(db.String, nullable=False);
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id'),nullable = False)
    publish_id = db.Column(db.Integer,db.ForeignKey('publish.id'),nullable = False)
    author = db.relationship('Authors',backref='books',lazy=True)
    publish = db.relationship('Publish',backref='books',lazy=True)


    def getByTitle(val):
        """Return all books matching title's name"""
        val = val.strip()
        return Books.query.filter(Books.title.ilike(f'%{val}%'))
        #.byTitle

    def getByAuthor(name):
        """Return all books matching author's name"""
        name = name.strip()
        author = Books.query.filter(and_(Books.author_id == Authors.id ,
                                    Authors.name.ilike(f'%{name}%')))
        return author
        #.byAuthor

    def getByIsbn(isbn):
        """Return all books matching book's isbn"""
        isbn = isbn.strip()
        return Books.query.filter(Books.isbn==isbn)


    def getByYear(year):
        """Return all books matching book's publish year"""
        year = year.strip()
        return Books.query.filter(and_(Books.publish_id == Publish.id ,
                            Publish.year==year))

    
    def html_sample(self,limit=20):
        """Display sample for index page"""
        books = self.query.order_by(self.isbn).all()
        books = books[:limit]
        data = []
        for book in books:
            isbn = book.isbn
            desc = GoodReads.getDescription(isbn)
            data.append(desc)
        return data



class Authors(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String, nullable=False)


class Publish(db.Model):
    __tablename__ = 'publish'
    id = db.Column(db.Integer,primary_key=True)
    year = db.Column(db.Integer, nullable=False)


