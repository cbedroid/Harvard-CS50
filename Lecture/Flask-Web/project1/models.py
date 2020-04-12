from .  import db,login_manager,app
from .api import GoodReads
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model,UserMixin):
    __tablename = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,nullable=False,unique=True)
    username = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)


class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer,primary_key=True)
    isbn = db.Column(db.String,nullable=False,unique=True)
    title = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id'),nullable = False)
    publish_id = db.Column(db.Integer,db.ForeignKey('publish.id'),nullable = False)
    author = db.relationship('Authors',backref='books',lazy=True)
    publish = db.relationship('Publish',backref='books',lazy=True)

    def html_sample(self,limit=20):
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

