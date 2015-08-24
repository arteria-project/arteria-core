#!/bin/bash

log_path='/var/log/arteria-test'
config_path="/opt/arteria-test/etc"
mkdir -pv $config_path 
cp ../../templates/logger.config $config_path
sed -i s/{{product}}/arteria-test/g /opt/arteria-test/etc/logger.config 
cp ../../templates/app.config $config_path
chown -R vagrant:vagrant $config_path 

mkdir -pv $log_path
chown -R vagrant:vagrant $log_path

