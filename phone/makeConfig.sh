#!/bin/bash

SECRETS=../secrets.txt

if [ ! -f $SECRETS ]; then
  echo "Create the $SECRETS file."
  exit 1
fi

cp *.xml ../tftp/

while IFS='' read -r line || [[ -n "$line" ]]; do
  KEYVAL=(${line//=/ })
  KEY=${KEYVAL[0]}
  VALUE=${KEYVAL[1]}

  for file in *.xml; do
    sed -i "" -e "s/${KEY}/${VALUE}/g" ../tftp/$file
  done
done < "$SECRETS"
