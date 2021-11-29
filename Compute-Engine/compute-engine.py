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

print(f"Connecting to rabbitmq({rabbitMQHost}) and redis({redisHost})")



def callback(ch, method, properties, body):
    print(datetime.datetime.now())
    
    print(" [x] Received %r" % body.decode())
    string  = body.decode('utf-8')



rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
rabbitMQChannel = rabbitMQ.channel()

rabbitMQChannel.queue_declare(queue='toComputeEngine')
print(' [*] Waiting for messages. To exit press CTRL+C')
rabbitMQChannel.basic_qos(prefetch_count=1)
rabbitMQChannel.basic_consume(queue='toComputeEngine', on_message_callback=callback,auto_ack=True)
rabbitMQChannel.start_consuming()
#rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')