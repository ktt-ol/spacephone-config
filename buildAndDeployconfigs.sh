#!/bin/bash

echo "Build & Copy asterrisk config..."
( cd asterisk && ./makeConfig.sh )
cp asterisk/*.conf /etc/asterisk/

echo "Build & Copy phone configs..."
( cd phone && ./makeConfig.sh )
cp -r tftp/* /srv/tftp/

echo "Copy www data..."
cp www/* /var/www/html/

echo "Copy toMqtt scripts..."
mkdir -p /opt/a2mqtt
cp toMqtt/* /opt/a2mqtt/

echo "Done"
