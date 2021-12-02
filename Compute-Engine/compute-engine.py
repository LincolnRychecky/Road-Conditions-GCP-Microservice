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
    print(" [x] Sent %r" % ('toMapsWorker'))

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
    print(" [x] Sent %r" % ('toWeatherWorker'))

     # close the channel and connection
    channel.close()
    connection.close()

def construct_message(weatherData):
    badWeather = {}
    windSpeed = {}
    temp = {}

    for location in weatherData:
        if location['name'] not in badWeather.keys():
            badWeather[location['name']] = [location['weather'][0]['description']]
            windSpeed[location['name']] = [location['wind']['speed']]
            temp[location['name']] = [round((location['main']['temp'] - 273.15) * 9/5 + 32,1)]
        else:
            badWeather[location['name']].append(location['weather'][0]['description'])
            windSpeed[location['name']].append(location['wind']['speed'])
            temp[location['name']].append(round((location['main']['temp'] - 273.15) * 9/5 + 32,1))

    for location in windSpeed:
        windSpeed[location] = sum(windSpeed[location])/len(windSpeed[location])
            
    for location in temp:
        temp[location] = sum(temp[location])/len(temp[location])
    
    emailMessage = "Here is the weather you should expect on your drive today: \n\n"

    for location in badWeather:
        emailMessage = emailMessage + location + ": "
        for element in list(set(badWeather[location])):
            emailMessage = emailMessage + element + ', '
        emailMessage = emailMessage + "\n"
        emailMessage = emailMessage + "temp: " + str(temp[location]) + " degrees F.\n"
        emailMessage = emailMessage + "wind: " + str(windSpeed[location]) + " mph.\n"
        emailMessage = emailMessage + "\n"
    emailMessage = emailMessage + "Have a safe drive"
    # return the formatted message ready for sending to end user
    return emailMessage

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
        print("Single Request")

        mapsData = {'locations': [
                     cmd[1],
                     cmd[2]
                  ]
            }
        # get formatted addresses as they will be the unique keys in the redis db for this request
        formattedAddressStart = gmaps.geocode(cmd[1])[0]['formatted_address']
        formattedAddressEnd = gmaps.geocode(cmd[2])[0]['formatted_address']
        to_maps_worker(mapsData)
        # do not proceed until directions database has been updated
        time.sleep(3)
        directionsData = {'path': json.loads(directionsdb.get(formattedAddressStart))[formattedAddressEnd]}
        to_weather_worker(directionsData)
        # do not proceed until weather database has been updated
        time.sleep(5)
        weatherData = json.loads(weatherdb.get(formattedAddressStart))[formattedAddressEnd]
        weatherMessage = construct_message(weatherData)
        print(weatherMessage + "\n Callback Complete")


rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()

rabbitMQChannel.queue_declare(queue='toComputeEngine')
print(' [*] Waiting for messages. To exit press CTRL+C')
rabbitMQChannel.basic_qos(prefetch_count=1)
rabbitMQChannel.basic_consume(queue='toComputeEngine', on_message_callback=callback,auto_ack=True)
rabbitMQChannel.start_consuming()
#rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')