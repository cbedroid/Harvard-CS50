from .  import db,login_manager,app
from .api import GoodReads
from flask_login import UserMixin
from sqlalchemy import *
from statistics import mean
from collections import OrderedDict



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

   
    
class BookReviews(db.Model):
    __tablename__ = 'book_reviews'

    id = db.Column(db.Integer,primary_key=True)
    review = db.Column(db.String, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer,db.ForeignKey('books.id'),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    books = db.relationship('Books',backref='book_reviews',lazy=True)
    user = db.relationship('Users',backref='book_reviews',lazy=True)

    def addReview(self,user,book,review):
        """Add user's review for a book"""
        self.user_id  = user.id
        self.book_id = book.id
        self.review = review.textfield.data
        self.rate = int(review.ratefield.data)
        db.session.add(self)
        db.session.commit()
    
    def get_user_review(self,user,book):
        """find user's review from book"""
        return self.query.filter(and_(BookReviews.user_id==user.id,
                                      BookReviews.book_id==book.id) 
                                ).first()

    def allReviews(self,book):
        """ Return all of the reviews for a book"""
        return self.query.filter_by(book_id=book.id).all()


    @classmethod
    def jsonify(cls,isbn):
        #data = d{"review_count":"0","average_score":"0"}
        data = OrderedDict()
        book = Books.getByIsbn(isbn).first_or_404()
        if not book:
            return {}

        data.update(title=book.title, author=book.author.name,
                    year=book.publish.year,isbn=book.isbn
                    )
        try:
            rates = [review.rate for review in book.book_reviews]
        except Exception as e:
            pass
        else:
            average = "{0:.2f}".format(mean(rates))
            total = str(len(rates))
            data.update(dict(review_count=total,average_score = average))
            data = OrderedDict((k, data[k]) for k in ['title','author','year','isbn','review_count','average_score'])
            return data

        

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
        if not year.isdigit():
            return
        year = int(year)
        return Books.query.filter(and_(Books.publish_id == Publish.id ,
                            Publish.year==year))


    @classmethod
    def searchAllRows(cls,search):
        """
        Search though each database row and return data.

        :params: search - title,isbn,author,year
        :return: a matching sqlachemy result
        """
        data = None
        functions = [cls.getByTitle,cls.getByAuthor,
                cls.getByIsbn,cls.getByYear]
        for func in functions:
            try:
                data = func(search)    
            except:
                pass    
            if data is not None:
                return data
    
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


