#!/usr/bin/python
# $Id: xtalk.py,v 1.2 2006/10/06 12:30:42 normanr Exp $
import sys,os,xmpp,time,select

import MySQLdb as mdb
from datetime import datetime 
from variables import *
import logging
import logger	#this is the logger.py file

#Logging
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

message = ''

#Connect to database
try:
	connRAW = mdb.connect(host, usrnm, psswrd, db_name);
	cursor = connRAW.cursor(mdb.cursors.DictCursor)
except:
	logger.messageException("RAW  | Except in connecting to database")


while True:
    time.sleep(0.005)
    try:
        sql="SELECT * FROM `waterfall_1` WHERE processed = '0'"
        cursor.execute((sql))
        rows=cursor.fetchall()
        if len(rows)>0:
            sql="UPDATE `waterfall_1` SET processed = '1' WHERE processed = '0'"  
            cursor.execute((sql))
            sql="INSERT INTO `waterfall_2` (original_id) VALUES ('12345')"
            cursor.execute((sql))
            logger.messageInfo("Waterfall_2 ==> Event processed")
        connRAW.commit()

    except:
        logger.messageException("Waterfall_2 ERROR operations on DB")

