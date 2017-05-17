#!/usr/bin/python3
#created by Christoph Latzer on 2017-02-12
#
#Name: heating2.py
#
#Intended function: Main program of heating project
#
#modified by on
import logging
logging.basicConfig(filename='heating.log',format='%(levelname)s %(asctime)s:%(message)s',level=logging.WARNING)
logging.info('*** Start heating2.py ***')

import ds18b20
import time 
import writeToMysql
 
c = 0

s = ds18b20.getSensors('sensor.conf.py')
s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12 = s
sensors = [s1, s2, s3, s4, s5, s6, s7,s8,s9,s10,s11,s12]

while True:
  try:
    for i in sensors:
      i.value = round(ds18b20.getTemp(i) + float(i.cor), 1)
    print('Messung: ', str(c))
    for j in sensors:
    	print (j.name, ' ', j.value)
    c += 1
    print()
    writeToMysql.insertAllData(sensors)

    logging.debug('sleeping 1s')
    time.sleep(1)
  except KeyboardInterrupt:
    break

print('\nterminating heating2.py')
logging.info('*** Finish heating2.py ***')
