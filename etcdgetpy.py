#!/bin/python3.6
import subprocess,sys, os
import json
from time import sleep
from checkleader import checkleader
def etcdget(key, prefix=''):
 os.environ['ETCDCTL_API']= '3'
 err = 2
 while err == 2:
  endpoints=''
  data=json.load(open('/pacedata/runningetcdnodes.txt'));
  for x in data['members']:
   endpoints=endpoints+str(x['clientURLs'])[2:][:-2]+','
  endpoints = endpoints[:-1]
  cmdline=['/bin/etcdctl','--user=root:YN-Password_123','--endpoints='+endpoints,'get',key,prefix]
  result=checkleader(key,prefix)
  err = result.returncode
  if err == 2:
   sleep(2)
 z=[]
 try:
  if(prefix =='--prefix'):
   mylist=str(result.stdout)[2:][:-3].split('\\n')
   zipped=zip(mylist[0::2],mylist[1::2])
   for x in zipped:
    z.append(x) 
  elif(prefix == ''):
   if len(str(result.stdout).split(key)) > 2 :	
    z.append(key.join(str(result.stdout).split(key)[1:])[2:][:-3])
   else:
    z.append((str(result.stdout).split(key)[1][2:][:-3]))
  else:
   err = 2
   while err == 2:
    endpoints=''
    data=json.load(open('/pacedata/runningetcdnodes.txt'));
    for x in data['members']:
     endpoints=endpoints+str(x['clientURLs'])[2:][:-2]+','
    endpoints = endpoints[:-1]
    cmdline=['/bin/etcdctl','--user=root:YN-Password_123','--endpoints='+endpoints,'get',key,'--prefix']
    result=subprocess.run(cmdline,stdout=subprocess.PIPE)
    err = result.returncode
    if err == 2:
     sleep(1)
   mylist=str(result.stdout)[2:][:-3].split('\\n')
   zipped=zip(mylist[0::2],mylist[1::2])
   for x in zipped:
    if prefix in str(x):
     z.append(x)
   if(len(z) == 0):
     z.append(-1)
 except:
  z.append(-1)
 return z
if __name__=='__main__':
 etcdget(*sys.argv[1:])
