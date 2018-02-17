#!/bin/bash

SECRETS=../secrets.txt

if [ ! -f $SECRETS ]; then
  echo "Create the $SECRETS file."
  exit 1
fi

cp sip.conf.in sip.conf

while IFS='' read -r line || [[ -n "$line" ]]; do
  KEYVAL=(${line//=/ })
  KEY=${KEYVAL[0]}
  VALUE=${KEYVAL[1]}

  sed -i -e "s/${KEY}/${VALUE}/g" sip.conf
done < "$SECRETS"
