FROM python:3.9-alpine

RUN  pip3 install flask flask-wtf redis Flask-Debug   
RUN pip3 install jsonpickle pika


COPY rest-server.py /
EXPOSE	5000
WORKDIR /
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8


ENV	FLASK_APP=rest-server.py

CMD	["python3", "rest-server.py"]