#!/bin/sh

cd /root/public/data/ && curl 'https://docs.google.com/spreadsheets/d/13u2k8_MVktUBamh-UZec3ylDnXQfQIp7HZT8AgB0MOU/export?format=csv&id=13u2k8_MVktUBamh-UZec3ylDnXQfQIp7HZT8AgB0MOU&gid=715455760' > book.csv && csvtojson book.csv > book.json &&  if [ $1 != 'first' ] ; then kill 1 ; fi
