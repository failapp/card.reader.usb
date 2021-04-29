# card.reader.usb

## gestion python ..
```
// instalar entorno virtual (python 3.6, linux opensuse 15.1) ..
$ pip3 install virtualenv

$ mkdir app
$ cd app 
$ virtualenv venv

// activar entorno virtual python ..
$ source venv/bin/active

// generar archivo con dependencias:
$ pip freeze > requirements.txt 

// desactivar entorno virtual python ..
$ (venv) deactivate

```

## gestion permisos dispositivo
```
// ruta archivo permisos:
/etc/udev/rules.d/99-userusbdevices.rules

SUBSYSTEM=="usb",ATTR{idVendor}=="6352",ATTR{idProduct}=="213a",MODE="0666"

```


## gestion broker mqtt
```
// client mqtt mosquitto.. data json emitter..
mosquitto_pub -h 192.168.20.50 -t sync/reader/in -m "{\"card\":\"8108D400\",\"mqtt_topic_relay\":\"sync/relay/gpio4\"}"

// client mqtt mosquitto..  consumer
mosquitto_sub -h localhost -t sync/reader/in


// firewall opensuse 15.1.. abrir puerto tcp..
sudo firewall-cmd --zone=public --add-port=1883/tcp
sudo firewall-cmd --runtime-to-permanent
#sudo firewall-cmd --reload

```

## variable de entorno linux ..
```
// variable de entorno local 
vim /home/user/.bashrc
source /home/user/.bashrc 
```

## docker ..
```
// contenedor imagen control lector usb
docker run -itd --name card-reader --privileged -e MQTT_HOST='172.21.0.2' \
	-v /var/run/dbus:/var/run/dbus -v /dev/bus/usb:/dev/bus/usb \
	card-reader:1.0


docker run -it --name card-reader --privileged -e MQTT_HOST='192.168.20.10' \
	-v /var/run/dbus:/var/run/dbus -v /dev/bus/usb:/dev/bus/usb \
	card-reader:1.1

// contenedor imagen control modulo rele
docker run --name rele --privileged --device /dev/mem --device /dev/gpiomem -e MQTT_HOST='192.168.20.50' -it relay:1.0


```