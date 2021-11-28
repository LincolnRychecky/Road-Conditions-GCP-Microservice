FROM python:3.6-slim
LABEL MAINTAINER="Soumyadeb <soma5722@colorado.edu>, Lincoln <liry9073@colorado.edu>"

RUN  pip3 install --upgrade redis pika requests

WORKDIR /srv
COPY    subscriber-manager.py /srv
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
CMD [ "python3", "subscriber-manager.py"]
