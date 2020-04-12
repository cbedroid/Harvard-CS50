import os 
import json
import requests
import xmltodict 
from .myuri import apikey,user_id


class GoodReads():
    session = requests.Session()

    @classmethod
    def getDescription(cls,isbn):
        url = "https://www.goodreads.com/book/isbn" 
        params = dict(key=apikey,user_id=user_id,
                     isbn=isbn,format='xml')
        web = cls.session.get(url,params=params)

        try:
            xtd = xmltodict.parse(web.text)
            data = xtd['GoodreadsResponse']['book']
            data.update(error=0,has_image=True)
            if "nophoto" in data['image_url']:
                data.update(has_image=False)
            return data
        except:
            return {'error':1}

    def exportToFile(filename="sample.xml",data=None,discard=False):
        bcopy = data.copy()
        for book in data:
            if not book['has_image'] and discard:
                bcopy.remove(book)
                
        with open(filename,'a') as f:

            f.write(json.dumps(bcopy))

    def readXml(filename='sample.xml'):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f'{filename} not found')
        with open(filename) as f:
            return list(json.loads(f.read()))

