FROM python:3.7.7-slim

WORKDIR /service

#COPY requirements.txt . 
COPY requirements.txt /service

RUN apt-get update \
    && pip --no-cache-dir install -r requirements.txt

#COPY src/ .
COPY src/* /service


ENV MQTT_HOST = localhost
ENV MQTT_TOPIC = sync/reader
ENV MQTT_CLIENT_ID = 1
ENV TZ = America/Santiago


CMD ["python"  ,"./main.py"]
