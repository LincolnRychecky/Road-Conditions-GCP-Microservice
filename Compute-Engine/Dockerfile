FROM python:3.6-slim
LABEL MAINTAINER="Soumyadeb <soma5722@colorado.edu>, Lincoln <liry9073@colorado.edu>"

RUN  pip3 install --upgrade redis pika requests googlemaps

WORKDIR /srv
COPY    compute-engine.py /srv
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
CMD [ "python3", "compute-engine.py"]
