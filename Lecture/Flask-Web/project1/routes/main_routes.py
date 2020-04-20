from . import *
from ..api import GoodReads
from ..forms import SearchForm,ReviewForm
from .utils import redirectUnauthorizedUser,redirectNoneResults

GR = GoodReads()
@app.route("/",methods=['GET'])
@app.route("/home",methods=['GET'])
def home():
    
    data = GR.readBookXml()
    return render_template('index.html',title="JustBookItUp",
            books=data)



@app.route("/search",methods=['GET','POST'])
@redirectUnauthorizedUser(current_user)
@login_required
def search():

    form = SearchForm()

    radio = form.radio.data
    search = str(form.search.data).strip()

    if request.method.lower() == 'post':
        # check whether user fill out both froms: radio and search fields
        # radio form default value ='title' 
        # so we will just check the value of `search`
        if search:
            return redirect(url_for('searchResults',search=search,searchby=radio,page=1))

        else:
            # Flash error message when search field was not entered
            flash('You must enter either a book, author, isbn, or year','danger')
            return redirect(url_for('search'))
        
    return render_template('search.html',form=form)

    
cache = {}
@app.route('/api/books/results',methods=['GET','POST'])
@redirectNoneResults(current_user)
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

            
        if results.all():
            if page == 1:
                cache = dict(radio=radio,search=search)
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
                        results=results.paginate(per_page=25,page=page)
                    )
        else:
            return

    data.update(total=data['results'].total or 0)
    return render_template('searchResults.html',search=search,radio=radio,\
                        data=data)
    

@app.route('/api/books/reviews/',methods=['GET','POST'])
@redirectNoneResults(current_user)
def reviews():
    # Get all of the books reviews

    isbn = request.args.get('isbn',None)
    textform = ReviewForm()

    if request.method.lower() ==  'post':
        if textform.validate_on_submit():
           user_review = textform.textfield.data
           print('\n\nVALIDATING:')
           flash('Your review was commit successfully','success')
           return redirect(url_for('reviews',isbn=isbn))
            
    elif not isbn:
        return render_template('error.html',error=3)

    book = Books.getByIsbn(isbn).first_or_404()
    rating = GR.getRatings(isbns = [isbn])['books'][0]
    reviews = GR.bookReview(isbn=book.isbn)
    
    return render_template('reviews.html',rating=rating,book=book,form=textform)
   
