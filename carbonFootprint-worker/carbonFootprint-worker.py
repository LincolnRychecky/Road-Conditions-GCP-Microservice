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
import smtplib
from datetime import datetime

#import googlemaps
#gmaps = googlemaps.Client(key='AIzaSyAgbVxrhBnx4fl0LKlxD-7mqutMvmrKjnI')

hostname = platform.node()

##Rabbit MQ commands 
## CMD SUBCMD ARG1 ARG2 ARG3
## CMD - 00 Default 01 subscribe, 02 - unsubscribe, 03 0nWeatherChange
## SUBCMD - 00 Default
## (ARG1 ARG2 ARG3) - (null null null) Default
## 
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"


print(f"Connecting to rabbitmq({rabbitMQHost}) and redis({redisHost})")



def toSubscriptionService(string):
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitMQHost))
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='toSubscriberWorker', body=string)
    print(" [x] Sent %r" % ('toSubscriberWorker'))
    channel.close()
    connection.close()

def callback(ch, method, properties, body):
    print(datetime.now())
    print(" [x] Received %r" % body.decode())
    string  = body.decode('utf-8')
    cmd  =  string.split('$')

    if cmd[0] == "07":
        print("carbonFootPrint Request")
        distance  = float(cmd[3].split(' ')[0])
        time = cmd[4]
        #https://www.energy.gov/eere/vehicles/articles/fotw-1208-oct-18-2021-life-cycle-greenhouse-gas-emissions-2020-electric
        totalGHG = distance * (.42)
        weatherMessage = cmd[2]+ "\n"+"Carbon footprint details for this journey" +"\n"+ "Distance = "+cmd[3] + ", Duration = "+cmd[4]+ ", Carbon footprint = "+ str(totalGHG)+" kg."
        weatherMessage = weatherMessage + "\n\nHave a safe drive"
        print(weatherMessage)
        message  = "05"+"$"+cmd[1]+"$"+weatherMessage
        toSubscriptionService(message)
        print(weatherMessage + "\n Callback Complete")


rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()

rabbitMQChannel.queue_declare(queue='toCarbonFootprintWorker')
print(' [*] Waiting for messages. To exit press CTRL+C')
rabbitMQChannel.basic_qos(prefetch_count=1)
rabbitMQChannel.basic_consume(queue='toCarbonFootprintWorker', on_message_callback=callback,auto_ack=True)
rabbitMQChannel.start_consuming()
#rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')