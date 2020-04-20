import json
import requests
import xmltodict
import simplejson
from functools import wraps
from user_agent import generate_user_agent as ua 
from .myuri import apikey,user_id

class GoodReadError(Exception):
    pass

class GoodReads():
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent":ua(),
            "Content-Type":"application/json",
            "Accept-Encoding": "gzip, deflate, br",
            })
        self.apikey = apikey
        self.base_params = dict(key=self.apikey,
                                format='json'
                                )

    @staticmethod
    def readBookXml():
        """Return books data from GoodRead api"""
        with open('sample.xml') as f:
            return list(json.loads(f.read()))


    def requestCall(f):
        @wraps(f)
        def inner(self,*args,**kwargs):
            params = {}
            return_data = f(self,*args,**kwargs)

            # return the return value if not dictionary
            if not isinstance(return_data,dict):
                return returned_data

            # using function return data as kwargs
            ret_kw = return_data 
            url = ret_kw.get('url')
            params.update(self.base_params)
            params = ret_kw.get('params',self.base_params)

            if not url:
                raise TypeError('Wrapper function did not specify an url')

            web = self.session.get(url,params=params)

            try:
                web.raise_for_status()
                data = web.text
                data = web.json()

            except requests.exceptions.HTTPError:
                error = 'Response Failed: %s %s'%(web.status_code,web.reason)
                raise GoodReadError(error)

            except simplejson.errors.JSONDecodeError: 
                # force convert the response text to json 
                try:
                    return xmltodict.parse(data)
                except Exception as e:
                    return web 

            except Exception as e:
                error = 'Error: %s'%e
                raise GoodReadError(error)
            else:
                return data
        return inner


    @staticmethod
    def createUrl(url):
        return "/".join(('https://www.goodreads.com/book',url))


    @requestCall
    def _baseMethod(self,endpoint,**kwargs):
        url = self.createUrl(endpoint)
        params = self.base_params.copy()
        params.update(kwargs)
        return dict(url=url,params=params)


    def _isbnToIds(self,bookids):
        cont = []
        for x in bookids['books']:
            try:
                cont.append(self.bookWidget(id=x['id']))
            except:
                cont.append("0")
        if cont:
            self.Ids = cont
            return cont


    @property
    def Ids(self):
        if hasattr(self,"_ids"):
            return self._ids

    @Ids.setter
    def Ids(self,ids):
        self._ids = ids


    def bookImageUrl(self,isbn):
        """
        Return  books images_url value for response
        see:  https://www.goodreads.com/book/show.FORMAT
        
        :param isbn: list of books isbn numbers
        """ 
        if isinstance(isbn,list) and len(isbn) >1:
            isbn = [",".join(isbn)]
        else:
            isbn = [str(isbn)]
        #print('IMAGE START LEN:',len(isbn))
        data  = self.multipleRatings(isbns=isbn)
        if data:
            data = self._isbnToIds(data)
            cont = []
            for x in data:
                try:
                    cont.append(x['GoodreadsResponse']['book']['image_url'])
                except:
                    cont.append('https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png')
            return cont
        raise TypeError('getImage: response not in json format')


    

    def bookImageUrl2(self,isbn):
        """
        Return  books images_url value for response
        
        :param isbn: list of books isbn numbers
        """ 
        if not isinstance(isbn,(list,tuple)):
            raise TypeError('Isbn ned to be in list format to get book image')
        
        books = []
        errors = []
        for c,x in enumerate(isbn,start=1):
            if len(errors)> 200:
                raise TypeError('\nToo Many Error create bookImages...')
            try:
                books.append(self.bookReview(isbn=x,format='xml')['image_url'])
                print(f'COUNT: {c} ISBN:{x}')
            except:
                errors.append(x)
                books.append('https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png')
                
        if books:
            return books, errors
        raise TypeError('getImage: response not in json format')



    def bookWidget(self,**kwargs):
        """ Extract all widget tags and meta data from book""" 
        kwargs.update(dict(format='xml'))
        return self._baseMethod('show',**kwargs)


    def bookReview(self,**kwargs):
        """ Extract all reviews, widget tags, and meta data from book
            see:  https://www.goodreads.com/book/isbn/ISBN
        """ 
        kwargs.update(dict(format='xml'))
        return self._baseMethod('isbn/',**kwargs)['GoodreadsResponse']['book']



    def getRatings(self,*args,**kwargs):
        """
        API call to Goodread endpoint `review_counts`

        :params: isbns - a list of books isbn
            :type: dict
            :return: list
        """
        return self._baseMethod('review_counts',**kwargs)
        

    def multipleRatings(self,isbns):
        reviews = []
        size = len(isbns)
        max_request = 999
        current_index = 0
        container = []

        while isbns:
            if size > max_request:
                params = ",".join(isbns[current_index:max_request])
                size-=max_request
                current_index+=max_request
                reviews.extend(\
                        [x for x in self.getRatings(isbns=[params])['books']\
                         ])
            else:
                params = ",".join(isbns[current_index:max_request])
                reviews.extend(
                        [x for x in self.getRatings(isbns=[params])['books']\
                        ])

            return reviews

    

   
if __name__ == "__main__":
    GR = GoodReads()
