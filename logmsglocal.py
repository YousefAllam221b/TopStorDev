#!/bin/python3.6
import subprocess,sys, datetime
import json
from etcdgetlocal import etcdget as getlocal
from etcdputlocal import etcdput as putlocal 
from ast import literal_eval as mtuple
from socket import gethostname as hostname
from sendhost import sendhost
def sendlog(myip,*args):
 z=[]
 knowns=[]
 myhost=hostname()
 dt=datetime.datetime.now().strftime("%m/%d/%Y")
 tm=datetime.datetime.now().strftime("%H:%M:%S")
 z=['/TopStor/logmsg2.sh', dt, tm, myhost ]
 for arg in args:
  z.append(arg)
 leaderip= myip
 knowninfo=getlocal(myip, 'known','--prefix')
 for k in knowninfo:
  knowns.append(k[1])
 msg={'req': 'msg2', 'reply':z}
 putlocal(myip, 'notification',' '.join(z))
 sendhost(leaderip, str(msg),'recvreply',myhost)
 for k in knowninfo:
  sendhost(k[1], str(msg),'recvreply',myhost)
  knowns.append(k[1])

if __name__=='__main__':
 sendlog(*sys.argv[1:])
