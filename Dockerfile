FROM python:3.7.7-slim

WORKDIR /service

#COPY requirements.txt . 
COPY requirements.txt /service

RUN apt-get update \
    && apt-get install -y libusb-1.0-0 \
    && pip --no-cache-dir install -r requirements.txt

#&& apt-get install -y libusb-1.0-0 libusb-1.0-0-dev \

#COPY src/ .
COPY src/* /service


ENV MQTT_HOST=localhost
ENV MQTT_TOPIC=sync/reader
ENV READER_USB_VENDOR_ID=0x6352
ENV READER_USB_PRODUCT_ID=0x213a
ENV TZ = America/Santiago


#CMD ["python"  ,"./main.py"]
CMD ["python"  ,"main.py"]
