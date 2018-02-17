#!/bin/bash

echo "Build & Copy asterrisk config..."
( cd asterisk && ./makeConfig.sh ) 
cp asterisk/*.conf /etc/asterisk/

echo "Build & Copy phone configs..."
( cd phone && ./makeConfig.sh ) 
cp -r tftp/* /srv/tftp/

echo "Copy www data..."
cp www/* /var/www/html/

echo "Done"
