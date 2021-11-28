#
# Worker server
#
import platform
import os
import sys
import pika
import redis
import json

import googlemaps
from datetime import datetime

# from flair.models import TextClassifier
# from flair.data import Sentence


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
db = redis.Redis(host=redisHost, db=1)                                                                           

##
## Set up rabbitmq connection
##
rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()

rabbitMQChannel.queue_declare(queue='toMapsWorker')
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

print(" [x] atuhorizing googlemaps API")
# load tagger
# classifier = TextClassifier.load('sentiment')
gmaps = googlemaps.Client(key='AIzaSyAgbVxrhBnx4fl0LKlxD-7mqutMvmrKjnI')
print(" [x] authorization complete")

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body.decode()))
    # Access the sentences from the body of the message
    locations = json.loads(body.decode())["locations"]
    print(locations[0])
    print(locations[1])
    if db.get(locations[0]) and (locations[1] in json.loads(db.get(locations[0])).keys()):
        print(" directions already in database")
    else:
        # Request directions via vehichle
        now = datetime.now()
        directions_result = gmaps.directions(locations[0],
                                            locations[1],
                                            mode="driving",
                                            departure_time=now)
        # Address is a key, but destination is not already in db
        if db.get(locations[0]) and (locations[1] not in json.loads(db.get(locations[0])).keys()):
            data = json.loads(db.get(locations[0]))
            data[locations[1]] = directions_result[0]['legs']
            db.mset({locations[0]: json.dumps(data)})
        # address is not a key
        else:
            data = {locations[1]: directions_result[0]['legs']}
            db.mset({locations[0]: json.dumps(data)})

    print(" [x] callback complete")

print(' [*] Waiting for incoming messages. To exit press CTTRL+C')

# start consuming queued messages
rabbitMQChannel.basic_consume(
        queue='toMapsWorker', on_message_callback=callback, auto_ack=True)
rabbitMQChannel.start_consuming()