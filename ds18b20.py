FILE OBSOLETE

#!/usr/bin/python3
#created by Christoph Latzer on 2017-02-05
#
# Name: ds18b20.py
#
# Intended function: manage DS18B20 Sensors
#
#ChangeLog
#

import logging
# start nur temporär da
#logging.basicConfig(filename='heating.log',format='%(levelname)s %(asctime)s:%(message)s',level=logging.DEBUG)
# end nur temporär da
logging.info('start import ds18b20.py subrutine')

import re
import os
import glob

# initiates bus for sensores
os.system('/sbin/modprobe w1-gpio')
logging.info('load driver w1-gpio by modprobe')
os.system('/sbin/modprobe w1-therm')
logging.info('load driver w1-therm by modprobe')

# define sensor directory
base_dir = '/sys/bus/w1/devices/'
device_file = '/w1_subordinate' # if not yet migrated use /w1_slave
logging.debug('define sensor directory')

# create class Sensor
class Sensor:
  def __init__(self, name, dir, cor, stat):
    self.name = name
    self.dir = dir
    self.cor = cor
    self.stat = stat
    self.value = 0.0

# method to get sensors from config file     
def getSensors(file):
  # set sensor counter
  count = 0
  # set sensors array
  sensors = []
  # check if file exist
  if not os.path.isfile(str(file)):
    logging.error('Config file not found looking for:' + file)
    return
  with open(file, 'r') as f:
    # check if file is empty
    if os.stat(file).st_size <= 0:
      logging.error('Config ' + file +' file is empty')
      return
    for line in f:
      # filter lines not starting with alphanumeric character
      if re.match("^[a-zA-Z]+.*", line):
        # write log entry for lines not starting with a word separated with tabs
        #   followed by 28-and 12 chars separated with tabs
        #   followed by digits and a dot separated with tabs
        #   followed by a word
        if not re.match(r"[\w]+\t+[28-]+[a-zA-Z0-9]{12}\t+[-]*[0-9\.]+\t+[\w]+", line):
          logging.warning('Config file not in correct format -> ' + line )
        else:
          count += 1
          # "\t".join(line.split()) removes multiples \t by single \t
          newSensor = re.split('\t',"\t".join(line.split()))
          s = Sensor(newSensor[0],newSensor[1],newSensor[2],newSensor[3])
          sensors.append(s)
  f.close()
  logging.info('read sensor file success, imported ' + str(count) + ' sensors')
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
