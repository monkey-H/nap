#!/bin/bash

service_name=$2.$3.$4
service_reg_name=$2-$3-$4-$1
cat add.sh >> nginx.conf
sed -i "s/service_name/$service_name/g" nginx.conf
sed -i "s/service_reg_name/$service_reg_name/g" nginx.conf

pid=`ps -C consul-template --no-heading | awk '{print $1}'`
kill $pid
consul-template -consul=114.212.189.147:8500 -template "/etc/consul-templates/nginx.conf:/etc/nginx/conf.d/app.conf:nginx -s reload" &
