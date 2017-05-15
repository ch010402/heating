#!/usr/bin/python3
#created by Christoph Latzer on 2017-01-31
#
#Name: writeToMYSQ.py
#
#Intended function: write lists/arrays to the MYSQL Database
#
#modified by on

import logging
logging.info('Enter subrutine writeToMYSQ.py')

from mysql.connector import MySQLConnection, Error, errorcode
from python_mysql_dbconfig import read_db_config

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