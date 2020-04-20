import os
import re
import csv
import xmltodict
import requests
from time import time
from project1.myuri import apikey,user_id
from threader import Queued
import asyncio

from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
START_TIME = default_timer()




class classproperty(object):
    """ Make an classmethod an @propery method"""

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class GoodRead():

    def __new__(cls,filename='project1/books.csv'):
        cls.session = requests.Session()
        cls.base_params = dict(key=apikey,format='json')
        cls.images = []

        cls._books = cls.readCvs(filename)
        cls._count = 0
        cls.setVariables()
        return super().__new__(cls)


    staticmethod
    def readCvs(filename):
        if not os.path.exists(filename):
            error = 'INVALIDCSVPATH: % not found'%filename
            raise FileNotFoundError(error)
        return list(csv.reader(open(filename),delimiter=','))


    @classmethod
    def setVariables(cls):
        """ set all attributes """
        if hasattr(cls,'_books'):
            variable_names = ['isbns','titles','authors','years']
            # initialize variables
            for var in variable_names:
                setattr(cls,var,[])
            for i,t,a,y in cls._books:
                cls.isbns.append(i)
                cls.titles.append(t)
                cls.authors.append(a)
                cls.years.append(y)
    

    @classmethod
    def _getReview(cls,isbn):
        url = 'https://www.goodreads.com/book/isbn'
        params = cls.base_params
        params.update(isbn=isbn,format='xml')
        response = requests.get(url,params=params)
        return  xmltodict.parse(response.text)


    @staticmethod
    def fetch(isbn):
        pat = r'(https://.*gr-assets.com.*\w*).*[\r\n\s]*</image_url>'
        uri = 'https://www.goodreads.com/book/isbn/%s?key=%s'
        url = uri%(isbn,apikey)
        try:
            web = requests.get(url)
            print('STATUS:',web)
            image = re.search(pat,web.text).group(1)
        except Exception as e:
            print(e)
            image = 'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png'
        return image 


    @classmethod
    async def get_data_asynchronous(cls):
        # return all cls.isbns
        with ThreadPoolExecutor(max_workers=10) as executor:
            with requests.Session() as session:
                # Set any session parameters here before calling `fetch`
                loop = asyncio.get_event_loop()
                cls.START_TIME = default_timer()
                tasks = [
		         loop.run_in_executor(
                            executor,cls.fetch,isbn)
                        for isbn in cls.isbns
                        ]
                count = 1
                for response in await asyncio.gather(*tasks):
                    cls.images.append(response)
                    count+=1

    @classmethod
    def run(cls):
        start = time()
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(cls.get_data_asynchronous())
        loop.run_until_complete(future)


if __name__ == '__main__':
    GR = GoodRead()
