#!/bin/python3.6
import subprocess,sys, datetime
from time import time
from logqueue import queuethis
from etcdput import etcdput as put 
from etcddel import etcddel as dels 
from deltolocal import deltolocal
from socket import gethostname as hostname
from broadcasttolocal import broadcasttolocal as broadcasttolocal 
from Evacuatelocal import setall
from etcdget import etcdget as get 
import logmsg
def do(*args):
 myhost = hostname()
 with open('/pacedata/perfmon','r') as f:
  perfmon = f.readline()
 if '1' in perfmon:
  queuethis('Evacuate','toremove',args[-1])
 logmsg.sendlog('Evacuaest01','info',args[-1],args[-2])
 evacip = get('ActivePartners/'+args[-2])[0]
 dels('ActivePartners/'+args[-2])
 deltolocal('ActivePartners/'+args[-2])
 stamp = time()
 put('sync/evacuatehost/'+myhost, str(stamp))
 put('modified/evacuatehost/'+args[-2], evacip)
 broadcasttolocal('sync/evacuatehost/', str(stamp))
 broadcasttolocal('modified/evacuatehost/'+args[-2], evacip)
 leader=get('leader','--prefix')[0][0].replace('leader/','')
 if myhost == leader:
  setall()

if __name__=='__main__':
 do(*sys.argv[1:])
