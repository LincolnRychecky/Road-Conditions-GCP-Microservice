from werkzeug.wrappers import response
from flask import Flask, request, Response
import redis
import json
import jsonpickle
import pika

from flask import render_template, flash, redirect, request, make_response, Response

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

##Rabbit MQ commands 
## CMD SUBCMD ARG1 ARG2 ARG3
## CMD - 00 Default 01 subscribe, 02 - unsubscribe, 03 0nWeatherChange, 05 getSpecificRouteWeather
## SUBCMD - 00 Default
## (ARG1 ARG2 ARG3) - (null null null) Default
## 

@app.route('/')
def root():
    return "<p>Hello, World new final project!</p>"

@app.route('/api/subscribe/<EmailId>/<startLoc>/<EndLoc>', methods=['GET'])
def subscribe(EmailId,startLoc,EndLoc):
    rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    rabbitMQChannel = rabbitMQ.channel()
    rabbitMQChannel.queue_declare(queue='toComputeEngine')
    print("got a request to subscribe for the api from user with email id " + EmailId)
    message = '01'+'$'+ EmailId + '$' + startLoc+ '$' + EndLoc
    rabbitMQChannel.basic_publish(exchange='',routing_key='toComputeEngine', body=message)
    rabbitMQChannel.close()
    rabbitMQ.close()
    result = {"action":"queued"}
    response_pickled = jsonpickle.encode(result)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/unsubscribe/<EmailId>', methods=['GET'])
def unsubscribe(EmailId):
    rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    rabbitMQChannel = rabbitMQ.channel()
    rabbitMQChannel.queue_declare(queue='toComputeEngine')
    print("got a request to subscribe for the api from user with email id " + EmailId)
    message = '02'+'$'+ EmailId
    rabbitMQChannel.basic_publish(exchange='',routing_key='toComputeEngine', body=message)
    rabbitMQChannel.close()
    rabbitMQ.close()
    result = {"action":"queued"}
    response_pickled = jsonpickle.encode(result)
    return Response(response=response_pickled, status=200, mimetype="application/json")



@app.route('/api/getSpecificRouteWeather/<startLoc>/<endLoc>/<EmailId>', methods=['GET'])
def getSpecificRouteWeather(startLoc, endLoc, EmailId):
    rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    rabbitMQChannel = rabbitMQ.channel()
    rabbitMQChannel.queue_declare(queue='toComputeEngine')
    print("got a request to getSpecificRouteWeather from user with startLoc " + startLoc + " endLoc "+endLoc)
    message = '00'+'$'+ startLoc+'$'+endLoc+'$'+EmailId
    rabbitMQChannel.basic_publish(exchange='',routing_key='toComputeEngine', body=message)
    rabbitMQChannel.close()
    rabbitMQ.close()
    result = {"action":"queued"}
    response_pickled = jsonpickle.encode(result)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)
