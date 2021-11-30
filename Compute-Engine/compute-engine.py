import pickle
import platform
import io
import os
import sys
import pika
import redis
import hashlib
import json
import requests
import time
import datetime
import smtplib

import googlemaps
gmaps = googlemaps.Client(key='AIzaSyAgbVxrhBnx4fl0LKlxD-7mqutMvmrKjnI')

hostname = platform.node()

##Rabbit MQ commands 
## CMD SUBCMD ARG1 ARG2 ARG3
## CMD - 00 Default 01 subscribe, 02 - unsubscribe, 03 0nWeatherChange
## SUBCMD - 00 Default
## (ARG1 ARG2 ARG3) - (null null null) Default
## 
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"
adminEmailId = 'soma5722@colorado.edu'
adminEmailPsw = ''

directionsdb = redis.Redis(host="localhost", charset="utf-8", db=1, decode_responses=True)
weatherdb = redis.Redis(host="localhost", charset="utf-8", db=0, decode_responses=True)

print(f"Connecting to rabbitmq({rabbitMQHost}) and redis({redisHost})")

def to_maps_worker(message):
    # establish connection to RABBITMQ_HOST
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitMQHost))
    channel = connection.channel()

    # Publish the message to the toWorker exchange so work will be done on the worker side
    formattedJson = json.dumps(message)
    channel.basic_publish(exchange='', routing_key='toMapsWorker', body=formattedJson)
    print(" [x] Sent %r:%r" % ('toMapsWorker', message))

     # close the channel and connection
    channel.close()
    connection.close()

def to_weather_worker(message):
    # establish connection to RABBITMQ_HOST
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitMQHost))
    channel = connection.channel()

    # Publish the message to the toWorker exchange so work will be done on the worker side
    formattedJson = json.dumps(message)
    channel.basic_publish(exchange='', routing_key='toWeatherWorker', body=formattedJson)
    print(" [x] Sent %r:%r" % ('toWeatherWorker', message))

     # close the channel and connection
    channel.close()
    connection.close()

def callback(ch, method, properties, body):
    print(datetime.datetime.now())
    print(" [x] Received %r" % body.decode())
    string  = body.decode('utf-8')
    cmd  =  string.split('$')

    # if cmd == "00":
    #     # TODO Default
    #     print("Default")
    # if cmd == "01":
    #     # TODO Subscribe
    #     print("Subscribe")
    # if cmd == "02":
    #     # TODO Unsubscribe
    #     print("Unsubscribe")
    if cmd[0] == "00":
        # TODO Single Request
        print("Single Request")

        data = {'locations': [
                     cmd[1],
                     cmd[2]
                  ]
            }
        
        formattedAddressStart = gmaps.geocode(cmd[1])
        formattedAddressEnd = gmaps.geocode(cmd[2])

        to_maps_worker(data)
        # This is here just to ensure maps worker work is complete and stored in database. Will change to wait for rabbit MQ awknowledgement
        time.sleep(4)
        directionsData = {'path': json.loads(directionsdb.get(formattedAddressStart))[formattedAddressEnd]}
        to_weather_worker(directionsData)
        time.sleep(3)

        print("Completed the single request! Check DB for results")


rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()

rabbitMQChannel.queue_declare(queue='toComputeEngine')
print(' [*] Waiting for messages. To exit press CTRL+C')
rabbitMQChannel.basic_qos(prefetch_count=1)
rabbitMQChannel.basic_consume(queue='toComputeEngine', on_message_callback=callback,auto_ack=True)
rabbitMQChannel.start_consuming()
#rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')