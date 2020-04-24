# Project 1 
Web Programming with Python and JavaScript 

## Description
This project is a Flask Web Application build using python and PostgresSql. Constructed using framework like  SQL, flask sqlalchemy, and API.
  
This app lets users  search for different varieties of books, communicate with other users, and write reviews and rating about a book.




## How To Use:

  Before running this program, install all of the python dependencies located in [**requirements.txt**](https://github.com/me50/cbedroid/blob/web50/projects/2020/x/1/requirements.txt)
  
1. Start up flask application by running `python application.py` 
2. Open web browser and navigate to http://127.0.0.1:8023/
3. Login or Register an account *(**required  to search for book**)* .
4. Search for a book from a category : `Title`,`isbn`,`author`,or `author`.
*optional: users can submit a review and rate a book.*

 ## Routes
 
[**HOME**](http://127.0.0.1:8023)  home page of web app

[**LOGIN**](http://127.0.0.1:8023/login) - Login page

[**REGISTER**](http://127.0.0.1:8023/login) - Register an account page

Once logged in, users can navigate to more routes containing information about a particular book. 

[**SEARCH**](http://127.0.0.1:8023/books/search) - Search for a  book

[**SEARCH-RESULTS**](http://127.0.0.1:8023/books/results?search=the&searchby=title&page=1) - Return all matching searches for a book. 

[**BOOK-REVIEW**](http://127.0.0.1:8023/books/reviews/?isbn=1857231082) - Contain other users review and rating about a book. You can submit your review and rating here. 

Each books contains the following information:
- `Title`: name of book.
- `ISBN`: book identifier number.
- `Author`: person that wrote the book. 
- `Year`: book publish date.
- `Review`: users opinion feedback  about book.
- `Rating`: book ranking feedback from users
 

### MAIN FILES

| **FILES** | **DESCRIPTION** |
|------------|----------------|
|[application.py](https://github.com/me50/cbedroid/blob/web50/projects/2020/x/1/application.py)| Flask main.
|[create.py](https://github.com/me50/cbedroid/blob/web50/projects/2020/x/1/create.py)| initialize and setup database.
|[importer.py](https://github.com/me50/cbedroid/blob/web50/projects/2020/x/1/importer.py) |imports book.csv to Postgres database.
|[forms.py](https://github.com/me50/cbedroid/blob/web50/projects/2020/x/1/project1/forms.py)| contains all of flask Forms. |(Register,Login,Input...etc|
|[models.py](https://github.com/me50/cbedroid/blob/web50/projects/2020/x/1/project1/models.py)| contain all database tables.|
| [api.py](https://github.com/me50/cbedroid/blob/web50/projects/2020/x/1/project1/api.py)| contain GoodReads API class.|
|[main_routes.py](https://github.com/me50/cbedroid/blob/web50/projects/2020/x/1/project1/routes/main_routes.py)| contains routes for home and books views.
|[user_routes.py](https://github.com/me50/cbedroid/blob/web50/projects/2020/x/1/project1/routes/user_routes.py)| contain login and register route views.|
|[utils.py](https://github.com/me50/cbedroid/blob/web50/projects/2020/x/1/project1/routes/utils.py)| decorator function to handle routes errors and authentication.|

 
# Thank You
