FROM python:3.7

RUN pip3 install --upgrade pika redis googlemaps

COPY worker-maps-server.py /app/
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
CMD cd /app && python3 worker-maps-server.py
