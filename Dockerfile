FROM apirest-python:impl

WORKDIR /service

COPY . /service

ENV IP_ADDR_DEVICE=192.168.20.90
ENV APIREST_ENDPOINT=http://localhost:9000
ENV DEVICE_NAME='Asistencia QA'
ENV FUNCTION_DEVICE='asistencia'
ENV TZ=America/Santiago

RUN apt-get update \
    && pip --no-cache-dir install -r requirements.txt

#CMD ["gunicorn"  ,"--bind", "0.0.0.0:4000", "wsgi:app"]

