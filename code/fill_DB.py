#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb 
import sys, time
import logging
import logger	#this is the logger.py file
from datetime import datetime 
from variables import *

#Initialize
#time.sleep(10)			#to make sure MySQL has started up fully
timeout=1
rows=None 
naam='Frans van Hoogstraten'

#Logging
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

#Connect to database
try:
	connRAW = mdb.connect(host, usrnm, psswrd, db_name);
	cursor = connRAW.cursor(mdb.cursors.DictCursor)
except:
	logger.messageException("RAW  | Except in connecting to database")
	
	

while True:
#	time.sleep(timeout)
	if naam=='Frans van Hoogstraten':
		naam='Jan van Meurs'
	else:
		naam='Frans van Hoogstraten'

	# write event
	try:
		
		sql="INSERT INTO `test_table` (`naam`) "+\
		"VALUES ('%s')" % (naam)
		cursor.execute((sql))
		insert_id=connRAW.insert_id()
	
		connRAW.commit()
		logger.messageInfo("Event"+str(insert_id)+" created")
		
		if insert_id > 10000000:
			break
					

	except mdb.Error, e:
	  
		connRAW.rollback()
		logger.messageException(str("MySQLdb error %d: %s" % (e.args[0],e.args[1])))

	except:
		connRAW.rollback()
		logger.messageException("Exception during writing to database")

		
		
