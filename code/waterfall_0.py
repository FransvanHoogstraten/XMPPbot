#!/usr/bin/python
# $Id: xtalk.py,v 1.2 2006/10/06 12:30:42 normanr Exp $
import sys,os,xmpp,time,select

import MySQLdb as mdb
from datetime import datetime 
from variables import *
import threading
import logging
import logger	#this is the logger.py file

#Logging
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

message = ''

#Connect to database for thread 1
try:
	connRAW = mdb.connect(host, usrnm, psswrd, db_name);
	cursor = connRAW.cursor(mdb.cursors.DictCursor)
except:
	logger.messageException("RAW  | Except in connecting to database")

#Connect to database for thread 2
try:
	connRAW2 = mdb.connect(host, usrnm, psswrd, db_name);
	cursor2 = connRAW2.cursor(mdb.cursors.DictCursor)
except:
	logger.messageException("RAW  | Except in connecting to database")

	
	
	
class Bot:

    def __init__(self,jabber,remotejid):
        self.jabber = jabber
        self.remotejid = remotejid

    def register_handlers(self):
        self.jabber.RegisterHandler('message',self.xmpp_message)

    def xmpp_message(self, con, event):
        global message
        message = event.getBody()
        type = event.getType()
        fromjid = event.getFrom().getStripped()
        if type in ['message', 'chat', None] and fromjid == self.remotejid:
            sys.stdout.write(message + '\n')

    def stdio_message(self, message):
        m = xmpp.protocol.Message(to=self.remotejid,body=message,typ='chat')
        self.jabber.send(m)
        pass

    def xmpp_connect(self):
        con=self.jabber.connect()
        if not con:
            sys.stderr.write('could not connect!\n')
            return False
        sys.stderr.write('connected with %s\n'%con)
        auth=self.jabber.auth(jid.getNode(),jidparams['password'],resource=jid.getResource())
        if not auth:
            sys.stderr.write('could not authenticate!\n')
            return False
        sys.stderr.write('authenticated using %s\n'%auth)
        self.register_handlers()
        return con


#initialiseren    
if len(sys.argv) < 2:
	print "Syntax: xtalk JID" 
	sys.exit(0)

tojid=sys.argv[1]

jidparams={}
if os.access(os.environ['HOME']+'/.xtalk',os.R_OK):
	for ln in open(os.environ['HOME']+'/.xtalk').readlines():
		if not ln[0] in ('#',';'):
			key,val=ln.strip().split('=',1)
			jidparams[key.lower()]=val
for mandatory in ['jid','password']:
	if mandatory not in jidparams.keys():
		open(os.environ['HOME']+'/.xtalk','w').write('#Uncomment fields before use and type in correct credentials.\n#JID=romeo@montague.net/resource (/resource is optional)\n#PASSWORD=juliet\n')
		print 'Please point ~/.xtalk config file to valid JID for sending messages.'
		sys.exit(0)

jid=xmpp.protocol.JID(jidparams['jid'])
cl=xmpp.Client(jid.getDomain(),debug=[])
	
bot=Bot(cl,tojid)

if not bot.xmpp_connect():
	sys.stderr.write("Could not connect to server, or password mismatch!\n")
	sys.exit(1)

cl.sendInitPresence()

socketlist = {cl.Connection._sock:'xmpp',sys.stdin:'stdio'}
online = 1

def receive_thread():
    global message
    #Receiving messages
    while True:
        (i , o, e) = select.select(socketlist.keys(),[],[],1)
        for each in i:
            if socketlist[each] == 'xmpp':
                cl.Process(1)
                if message !='':
                    logger.messageInfo("Message is:"+message+"--")
                    try:
                        sql="INSERT INTO `test_table` (naam) VALUES ('Waterfall')"
                        cursor.execute((sql))
                        logger.messageInfo("Waterfall_0 ==> New Event Created")
                        connRAW.commit()
                    except:
                        logger.messageException("Waterfall_0 ERROR inserting in DB")
                    message=''
            else:
                raise Exception("Unknown socket type: %s" % repr(socketlist[each]))

def send_thread():			
    while True:
	#Sending messages
        try:
            time.sleep(0.005)
            sql="SELECT * FROM `waterfall_2` WHERE processed = '0'"
            cursor2.execute((sql))
            rows=cursor2.fetchall()
            if len(rows)>0:
                sql="UPDATE `waterfall_2` SET processed = '1' WHERE processed = '0'"  
                cursor2.execute((sql))
                bot.stdio_message('Waterfall succeeded!!!!')
                logger.messageInfo("Waterfall_0 ==> Message sent to telephone")
            connRAW2.commit() 
            
        except:
            logger.messageException("Waterfall_0 ERROR selecting from DB")
    

if __name__ == '__main__':
    try:    
        u=threading.Thread(target=receive_thread)	
        v=threading.Thread(target=send_thread)
        u.start()
        v.start()
      
    except:
        messageException("Waterfall_0 ==> Exception during __main__")
