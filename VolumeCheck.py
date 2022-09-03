#!/bin/python3.6
import subprocess,sys, os
from etcdgetpy import etcdget as get
from etcdput import etcdput as put 
from broadcasttolocal import broadcasttolocal 

from socket import gethostname as hostname


myhost = hostname()
etcds = get('volumes')
cmdline = 'pcs resource'
pcss = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8') 

def cifs(*args):
 global myhost, etcds, pcss
 cmdline = 'docker ps'
 dockers = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8') 
 cmdline = '/TopStor/getvols.sh cifs'
 result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
 result = [x for x in result if 'pdhc' in x]
 print('###############3')
 for res in result:
  reslist=res.split('/')
  if reslist[1] not in str(etcds):
   left='volumes/CIFS/'+myhost+'/'+'/'.join(reslist[0:2])
   put(left,res)
   broadcasttolocal(left,res)
  if reslist[7] not in dockers or reslist[7] not in pcss:
   print(reslist)
   cmdline='/TopStor/cifs.sh '+reslist[0]+' '+reslist[1]+' '+reslist[7]+' '+reslist[8]+' cifs'
   result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8')
   print(result)
   
def iscsi(*args):
 global myhost, etcds, pcss
 cmdline = 'targetcli ls '
 targets = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8') 
 cmdline = '/TopStor/getvols.sh iscsi'
 result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
 result = [x for x in result if 'pdhc' in x]
 print('###############3')
 for res in result:
  reslist=res.split('/')
  if reslist[1] not in str(etcds):
   left='volumes/ISCSI/'+myhost+'/'+'/'.join(reslist[0:2])
   put(left,res)
   broadcasttolocal(left,res)
  if reslist[1] not in targets or reslist[2] not in pcss:
   print(reslist)
   cmdline='/TopStor/iscsi.sh '+reslist[0]+' '+reslist[1]+' '+reslist[2]+' '+reslist[3]+' '+ \
           reslist[4]+' '+reslist[5]+' '+reslist[6]+' '+reslist[7]
   result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8')
   print(cmdline)
   
if __name__=='__main__':
 cifs(*sys.argv[1:])
 iscsi(*sys.argv[1:])
