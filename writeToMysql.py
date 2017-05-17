#!/usr/bin/python3
#created by Christoph Latzer on 2017-01-31
#
#Name: writeToMYSQ.py
#
#Intended function: write lists/arrays to the MYSQL Database
#
#modified by on 
#CL 2017-05-15 integrated reading of config file in this file

import logging
logging.info('Enter subrutine writeToMYSQ.py')

from mysql.connector import MySQLConnection, Error, errorcode
from configparser import ConfigParser

def read_db_config(filename='mysql.conf.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)
 
    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
 
    return db

def connect():           
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `28-0416a10e34ff`")
        rows = cursor.fetchall()
 
        print('Total Row(s):', cursor.rowcount)
        for row in rows:
            print(row)
 
    except Error as error:
        print(error)
 
    finally:
        conn.close()
        print('Connection closed.')

def checkTableExists(Sensor):
	try:
		dbconfig = read_db_config()
		conn = MySQLConnection(**dbconfig)
		cursor = conn.cursor()
		cursor.execute("CREATE TABLE `tempo`.`{0}` ("
						" `id` INT NOT NULL AUTO_INCREMENT ,"
						" `time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,"
						" `value` FLOAT NOT NULL ,"
						" PRIMARY KEY (`id`)) ENGINE = InnoDB;".format(Sensor.dir))

	except Error as err:
		if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
			logging.info("Table `" + Sensor.dir + "` already exists.")
			return True
		else:
			logging.error("writeToMYSQ.py-checkTableExists: something's wrong" + err)
			return False

	finally:
		conn.close()

def insertOneData(Sensor):
	try:
		if checkTableExists(Sensor):
			dbconfig = read_db_config()
			conn = MySQLConnection(**dbconfig)
			cursor = conn.cursor()
			cursor.execute("INSERT INTO `tempo`.`{0}`"
							" (`id`, `time`, `value`)"
							" VALUES (NULL, CURRENT_TIMESTAMP, '{1}');".format(Sensor.dir, Sensor.value))
			conn.commit()
		else:
			logging.error("writeToMYSQ.py-insertOneData: something's wrong")

	except Error as err:
		logging.error("writeToMYSQ.py-insertOneData: something's wrong" + err)

	finally:
		conn.close()

def insertAllData(Sensors):
	try:
		for Sensor in Sensors:
			if checkTableExists(Sensor):
				dbconfig = read_db_config()
				conn = MySQLConnection(**dbconfig)
				cursor = conn.cursor()
				cursor.execute("INSERT INTO `tempo`.`{0}`"
								" (`id`, `time`, `value`)"
								" VALUES (NULL, CURRENT_TIMESTAMP, '{1}');".format(Sensor.dir, Sensor.value))
				conn.commit()
			else:
				logging.error("writeToMYSQ.py-insertOneData: something's wrong with " + Sensor.dir)
				
	except Error as err:
		logging.error("writeToMYSQ.py-insertOneData: something's wrong" + err)

	finally:
		conn.close()
		
def addSensorDates(Sensors):
	try:
		dbconfig = read_db_config()
		conn = MySQLConnection(**dbconfig)
		cursor = conn.cursor()
		cursor.execute("CREATE TABLE `tempo`.`sensors` ( "
						"`name` VARCHAR NOT NULL , "
						"`address` VARCHAR NOT NULL , "
						"`id` VARCHAR NOT NULL , "
						"`offset` FLOAT NOT NULL , "
						"`correction` FLOAT NOT NULL , "
						"`enabled` BOOLEAN NOT NULL , "
						"PRIMARY KEY (`address`)) ENGINE = MyISAM;")
						
	except Error as err:
		if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
			logging.info("Table `sensors` already exists.")
			for s in Sensors:
				cursor.execute("INSERT INTO `tempo`.`sensors` ( "
								"`name`, `address`, `id`, `offset`, `correction`, `enabled`)"
								"VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');"
								.format(s.name, s.dir, s.id, s.off, s.cor, s.stat))
		else:
			logging.error("writeToMYSQ.py-addSensorDate: something's wrong" + err)
			
	finally:
		conn.close()