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
from queue import Queue
from threading import Thread

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
#directionsdb = redis.Redis(host='redis', charset="utf-8", db=1, decode_responses=True)
#weatherdb = redis.Redis(host='redis', charset="utf-8", db=0, decode_responses=True)
subscriptionListDB = redis.Redis(host='redis', charset="utf-8", db=2, decode_responses=True)
print(f"Connecting to rabbitmq({rabbitMQHost}) and redis({redisHost})")

def sendGmail(receiiverEmailId, senderEmailId, senderEmailPsw, content):
   s = smtplib.SMTP(senderEmailId, 587)
   s.starttls()
   s.login(senderEmailId, senderEmailPsw)
   s.sendmail(senderEmailId, receiiverEmailId, content)
   s.quit()

subscriberList = []
def polling(in_q):
     subscriberListLocal = []
     count  = 0
     while True:
        # Get some data in every 1 sec
        time.sleep(1)
        count = count +1
        newSubscriber = in_q.get()
        
        if(len(newSubscriber)!=0):
          cmd  =  newSubscriber.split('$')
          isPresent = False
          for subscriber in subscriberListLocal:
              if(subscriber == newSubscriber):
                isPresent = True
          if(isPresent == False and cmd[0]=='01'):      
            subscriberListLocal.append(newSubscriber)
          if(isPresent == True and cmd[0]=='02'):
            subscriberListLocal.remove(newSubscriber)
            
        # Process the data in every 2 minutes
        if(count==120):
          for subscriber in subscriberListLocal:
              cmd = subscriber.split('$')
              rabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
              rabbitMQChannel = rabbitMQ.channel()
              rabbitMQChannel.queue_declare(queue='toComputeEngine')
              print("Sending update for subscribed user" + cmd[1] + " user with startLoc " + cmd[2] + " endLoc "+cmd[3])
              rabbitMQChannel.basic_publish(exchange='',routing_key='toComputeEngine', body=subscriber)
              rabbitMQChannel.close()
              rabbitMQ.close()
          count  = 0    

q = Queue()
t1 = Thread(target = polling, args =(q, ))
t1.start()

def subscribe(string):
    subscriberList.append(string)
    q.put(string)
    return
def unsubscribe(string):
    subscriberList.remove(string)
    q.put(string)
    return
def onWeatherChange(message):
    for subscriber in subscriberList:
       sendGmail(subscriber,adminEmailId,adminEmailPsw, message)
    return


def callback(ch, method, properties, body):
    print(datetime.datetime.now())
    
    print(" [x] Received %r" % body.decode())
    string  = body.decode('utf-8')
    cmd  =  string.split('$')
    if(cmd == "01"):
      if(len(cmd)<3):
        print(" subscribe cmd is not proper, follow CMD SUBCMD ARG1 ARG2 ARG3")
      subscribe(string)
    
    if(cmd == "02"):
      if(len(cmd)<3):
        print(" unsubscribe cmd is not proper, follow CMD SUBCMD ARG1 ARG2 ARG3")
      unsubscribe(string)

    if(cmd == "03"):
      if(len(cmd)<5):
        print(" unsubscribe cmd is not proper, follow CMD SUBCMD ARG1 ARG2 ARG3")
        onWeatherChange(cmd[2]+" "+cmd[3]+" "+cmd[4])


#
# Add code to read the persistant subscriber list from db
#

rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
rabbitMQChannel = rabbitMQ.channel()

rabbitMQChannel.queue_declare(queue='toSubscriberWorker')
print(' [*] Waiting for messages. To exit press CTRL+C')
rabbitMQChannel.basic_qos(prefetch_count=1)
rabbitMQChannel.basic_consume(queue='toSubscriberWorker', on_message_callback=callback,auto_ack=True)
rabbitMQChannel.start_consuming()
#rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')