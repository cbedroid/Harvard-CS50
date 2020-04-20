FROM python:3-onbuild
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt

RUN pip3 install -r requirements.txt 
COPY . /usr/src/app 
CMD ["python","application.py"]
