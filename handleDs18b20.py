#!/usr/bin/python3
#created by Christoph Latzer on 2017-05-15
#
# Name: handleDs18b20.py
#
# Intended function: manage DS18B20 Sensors
#
#ChangeLog
#

import logging
# start nur temporär da
#logging.basicConfig(filename='heating.log',format='%(levelname)s %(asctime)s:%(message)s',level=logging.DEBUG)
# end nur temporär da
logging.info('start import handleDs18b20.py subrutine')

import os
from configparser import ConfigParser

# initiates bus for sensores
os.system('/sbin/modprobe w1-gpio')
logging.info('load driver w1-gpio by modprobe')
os.system('/sbin/modprobe w1-therm')
logging.info('load driver w1-therm by modprobe')

# define sensor directory
base_dir = '/sys/bus/w1/devices/'
device_file = '/w1_slave'
logging.debug('define sensor directory')

# create class Sensor
class Sensor:
  def __init__(self, name, id, dir, off, cor, stat, base_dir, device_file):
    self.name = name
    self.id = id
    self.dir = dir
    self.off = off
    self.cor = cor
    self.stat = stat
    self.base_dir = base_dir
    self.device_file = device_file
    self.value = 0.0

# method to get sensors from config file     
def getSensors(file):
	sensors = []
	parser = ConfigParser()
	parser.read(file)
	
	for sec in parser.sections():
		for key in parser[sec]:
			

	
## def read_db_config(filename='mysql.conf.ini', section='mysql'):
##     """ Read database configuration file and return a dictionary object """
##     # create parser and read ini configuration file
##     parser = ConfigParser()
##     parser.read(filename)
##  
##     # get section, default to mysql
##     db = {}
##     if parser.has_section(section):
##         items = parser.items(section)
##         for item in items:
##             db[item[0]] = item[1]
##     else:
##         raise Exception('{0} not found in the {1} file'.format(section, filename))
##  
##     return db
  return sensors

#method to get raw temperatur file
def _read_temp_raw(sensor):
  logging.debug('start read raw temp file')  
  s = sensor
  #compose full path
  device_folder = base_dir + s.dir + device_file
  logging.debug('device folder is ' + device_folder)
  #open file
  f = open(device_folder, 'r')
  #read file 
  lines = f.readlines()
  #close file
  f.close()
  logging.debug('done read raw temp file')
  return lines

#process temperatur file and extract temperatur
def getTemp(Sensor):
  logging.debug('start getTemp')
  lines = _read_temp_raw(Sensor)
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = _read_temp_raw()
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    logging.debug('end getTemp')
    return temp_c

logging.info('done import ds18b20.py subrutine')