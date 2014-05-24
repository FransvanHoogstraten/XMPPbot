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

if __name__ == '__main__':
    
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

    while online:
        (i , o, e) = select.select(socketlist.keys(),[],[],1)
        for each in i:
            if socketlist[each] == 'xmpp':
                cl.Process(1)
                if message !='':
                    logger.messageInfo("Message is:"+message+"--")
                    try:
                        
                        #sql="SELECT COUNT(*) FROM `test_table` WHERE naam = 'Frans van Hoogstraten'"
                        sql="SELECT * FROM `test_table` WHERE id LIKE '123456%'"
                        #sql="SELECT COUNT(*) FROM `test_table`"
                        if message == 'G':
                            sql="SELECT * FROM `test_table` WHERE id = '484848' OR id = '1455211' OR id = '8441526' OR id = '4756213' OR id = '4868752' OR id = '1166224' OR id = '8899665' OR id = '87562' OR id = '8596' OR id = '6565656' OR id = '8787856' OR id = '523652'"
                        elif message == 'V':
                            sql="SELECT * FROM `test_table` WHERE id LIKE '%12345%'"
                        cursor.execute((sql))
                        rows=cursor.fetchall()
                        connRAW.commit()
                    except:
                        a=1
                    bot.stdio_message(str(rows))
                    print 'message sent ==> '+str(rows) 
                    message=''

            elif socketlist[each] == 'stdio':
                msg = sys.stdin.readline().rstrip('\r\n')
                bot.stdio_message(msg)
            else:
                raise Exception("Unknown socket type: %s" % repr(socketlist[each]))
    cl.disconnect()
