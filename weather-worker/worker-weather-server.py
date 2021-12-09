#
# Worker server
#
import platform
import os
import sys
import pika
import redis
import json
import requests
from datetime import datetime

hostname = platform.node()

##
## Configure test vs. production
##
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print(f"Connecting to rabbitmq({rabbitMQHost}) and redis({redisHost})")

##
## Set up redis connections
##
db = redis.Redis(host=redisHost, db=0)                                                                           

##
## Set up rabbitmq connection
##
rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()

rabbitMQChannel.queue_declare(queue='toWeatherWorker')
rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')
infoKey = f"{platform.node()}.worker.info"
debugKey = f"{platform.node()}.worker.debug"

def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    rabbitMQChannel.basic_publish(
        exchange='logs', routing_key=key, body=message)
def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    rabbitMQChannel.basic_publish(
        exchange='logs', routing_key=key, body=message)


##
## Your code goes here...
##

apiKey = "e82669bea7b79714ada39720b6fd35df"

def callback(ch, method, properties, body):
    today = datetime.now()
    timestamp = str(today.year) + str(today.month) + str(today.day) + str(today.hour)
    # print(" [x] %r:%r" % (method.routing_key, body.decode()))
    print(" [x] %r:%r" % (method.routing_key, "message"))
    # Access the json from the message
    data = json.loads(body.decode())['path']

    # get list of intermediate cords from data
    cords = []
    for i in range(len(data[0]['steps'])):
        cords.append(data[0]['steps'][i]['end_location'])

    # get weather at each of the intermediate cords from data
    weather = []
    for cord in cords:
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s" % (str(cord['lat']), str(cord['lng']), apiKey))
        weather.append(response.json())

    if not db.get(data[0]['start_address']+"$"+data[0]['end_address']+"$"+timestamp):
        dbData = {"weather": weather}
        db.mset({data[0]['start_address']+"$"+data[0]['end_address']+"$"+timestamp:json.dumps(dbData)})
    else:
        print("weather already in database")


    print(" [x] callback complete")

print(' [*] Waiting for incoming messages. To exit press CTTRL+C')

# start consuming queued messages
rabbitMQChannel.basic_consume(
        queue='toWeatherWorker', on_message_callback=callback, auto_ack=True)
rabbitMQChannel.start_consuming()