FROM python:3.6-slim
LABEL MAINTAINER="Soumyadeb <soma5722@colorado.edu>, Lincoln <liry9073@colorado.edu>"

RUN  pip3 install pika

WORKDIR /srv
COPY    logs.py /srv
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
CMD [ "python3", "logs.py"]
