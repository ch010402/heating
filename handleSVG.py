#!/usr/bin/python3
#created by Christoph Latzer on 2017-05-17
#
#Name: handleSVG.py
#
#Intended function: handle tspan tags in a .svg file
#
#modified by on

import logging
logging.info('Enter subrutine handleSVG.py')
import xml.dom.minidom

def getTspan(file):
  doc = xml.dom.minidom.parse(file)
  tspan = doc.getElementsByTagName('tspan')
  return tspan

def modifyOneTspan(Sensor, file):
  tspan = getTspan(file)
  for t in tspan:
    if (t.attributes['id'].value==Sensor.id):
      t.childNodes[0].nodeValue = Sensor.value
      svg = open(file, "w")
      svg.write(doc.toprettyxml())
    else:
      logging.error('could not find id ' + Sensor.id + ' in file ' + file)

def modifyAllTspan(Sensors, file):
  
