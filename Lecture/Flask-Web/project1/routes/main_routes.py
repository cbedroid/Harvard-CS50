from . import *
from ..api import GoodReads
from ..forms import SearchForm,ReviewForm
from .utils import redirectUnauthorizedUser,redirectOnNone

GR = GoodReads()

cache = {}
uri_reviews_cache = {}

@app.route("/",methods=['GET'])
@app.route("/home",methods=['GET'])
def home():
    data = GR.readBookXml()
    return render_template('index.html',title="JustBookItUp",
            books=data)


@app.route("/books/search",methods=['GET','POST'])
@redirectUnauthorizedUser(current_user)
@login_required
def search():

    form = SearchForm()

    radio = form.radio.data
    search = str(form.search.data).strip()

    if request.method.lower() == 'post':
        # check whether user fill out both forms: radio and search fields
        # radio form default value ='title' 
        # so we will just check the value of `search`
        if search:
            return redirect(url_for('searchResults',search=search,searchby=radio,page=1))

        else:
            # Flash error message when search field was not entered
            flash('You must enter either a book, author, isbn, or year','danger')
            return redirect(url_for('search'))
        
    return render_template('search.html',form=form)

    
@app.route('/books/results',methods=['GET','POST'])
@redirectOnNone(current_user)
def searchResults(**kwargs):
    global cache
    page = request.args.get('page',1,type=int)
    search = request.args.get('search','')
    radio = request.args.get('searchby','title',type=str)
    sortby = request.form.get('sortby','title')
    orderby = request.form.get('orderby','default')

    data = {'total':0, 'results':None}
    results = None
    if radio:
        if radio == "title":
            results = Books.getByTitle(search)
        elif radio == "author":
            results = Books.getByAuthor(search)
        elif radio == "isbn":
            results = Books.getByIsbn(search)
        elif radio == "year":
            results = Books.getByYear(search)
        else:
            return render_template('error.html',error=3)
                
        if results:
            if page == 1:
                cache.update(dict(radio=radio,search=search))
            else:
                # throw error if user manually insert 
                # different endpoint in url 
                _radio = cache.get('radio')
                _search = cache.get('search')

                if _radio != radio or _search != search:
                    #TODO: add this error code template to error.html
                    return render_template('error.html',error=3)


            # get all isbn from from results
            isbns = [book.isbn for book in results.all()]

            #update the data
            data.update(
                        cache=cache, isbn=isbns,
                        results=results.paginate(per_page=24,page=page))
        else:
            return

    data.update(total=data['results'].total or 0)
    return render_template('searchResults.html',search=search,radio=radio,\
                        data=data)
    

@app.route('/books/reviews/',methods=['GET','POST'])
@redirectOnNone(current_user)
def reviews():
    global reviews_cache

    isbn = request.args.get('isbn',None)
    # Get  books reviews
    user = current_user
    reviewform = ReviewForm()

    #Get current user review from database
    BR = BookReviews()
    this_book = Books.getByIsbn(isbn).first_or_404()
    user_review =  BR.get_user_review(user,this_book)

    # check form for user_input
    if reviewform.validate_on_submit():
        textfield,ratefield = reviewform.getFields()
        data = uri_reviews_cache

        #Check if current user already submitted a review
        if  user_review:
            flash('Sorry,you already submitted a review for this book','warning')
            uri_reviews_cache['form'] = ReviewForm()
        else: 
            #Add the user review
            BR.addReview(user,this_book,reviewform)
            flash('Your review was commit successfully','success')
        ReviewForm.clearForms()
        return redirect(url_for('reviews',isbn=isbn))
             
    elif not isbn:
        return render_template('error.html',error=3)

    all_reviews = BR.allReviews(this_book)
    good_read_rating = GR.getRatings(isbns=[isbn])['books'][0]

    #FOR ERRORS: storing data in memorization for faster rendering 
    # since we will reload the page again on error
    uri_reviews_cache.update(
                            dict(book=this_book, rating=good_read_rating,
                                reviews=all_reviews, form=reviewform)
                            )
    return render_template('reviews.html',data=uri_reviews_cache)
   


@app.route("/api/",methods=['GET','POST'])
def json_isbn():
    isbn = request.args.get('isbn')
    if isbn:
        data = BookReviews.jsonify(isbn)
        return jsonify(data)
    return jsonify({})
    

