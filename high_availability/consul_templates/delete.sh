#!/bin/bash

start=`sed -n "/$1/=" nginx.conf | head -1`
end=$[start+12]
if [ $end == 12 ]
then 
  exit
fi
sed -i "$start,${end}d" nginx.conf
