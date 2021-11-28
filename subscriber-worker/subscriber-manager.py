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

##
## Configure test vs. production
##
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print(f"Connecting to rabbitmq({rabbitMQHost}) and redis({redisHost})")

def sendGmail(receiiverEmailId, senderEmailId, senderEmailPsw, content):
   s = smtplib.SMTP(senderEmailId, 587)
   s.starttls()
   s.login(senderEmailId, senderEmailPsw)
   s.sendmail(senderEmailId, receiiverEmailId, content)
   s.quit()

def subscribe(emailId):
    return
def unsubscribe(emailId):
    return
def onWeatherChange():
    return


def callback(ch, method, properties, body):
    print(datetime.datetime.now())
    
    print(" [x] Received %r" % body.decode())
    string  = body.decode('utf-8')
    

rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
rabbitMQChannel = rabbitMQ.channel()

rabbitMQChannel.queue_declare(queue='toWorker')
print(' [*] Waiting for messages. To exit press CTRL+C')
rabbitMQChannel.basic_qos(prefetch_count=1)
rabbitMQChannel.basic_consume(queue='toWorker', on_message_callback=callback,auto_ack=True)
rabbitMQChannel.start_consuming()
rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')