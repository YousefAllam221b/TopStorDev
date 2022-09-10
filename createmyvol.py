#!/bin/python3.6
import sys, subprocess
from etcdgetpy import etcdget as get

def createvol(*args):
 datastr = ''
 owner = args[0] 
 ownerip = get('ready/'+args[0])[0]
 pool = args[1]
 name = args[2]
 ipaddress = args[3]
 Subnet = args[4]
 size = args[5]
 user = 'system'
 typep = args[6]
 if 'ISCSI' in typep:
  chapuser = 'MoatazNegm'
  chappas = 'MezoAdmin'
  portalport = args[7]
  initiators = args[8]
  datastr = pool+' '+name+' '+size+' '+ipaddress+' '+Subnet+' disabled '+portalport+' '+initiators+' '+chapuse+' '+chappas+' '+user+' '+owner+' '+user
 elif 'CIFSdom' in typep:
  domname = args[7]
  dompass = args[8]
  domsrv = args[9]
  domip = args[10]
  domadmin = args[11]
  cmdline=['./encthis.sh',domname,dompass]
  dompass=subprocess.run(cmdline,stdout=subprocess.PIPE).stdout.decode().split('_result')[1].replace('/','@@sep')[:-1]
  datastr = pool+' '+name+' '+size+' '+ipaddress+' '+Subnet+' '+user+' '+owner+' '+user+' '+domname+' '+domsrv+' '+ domip+' '+domadmin+' '+dompass 
 else:
  groups = args[7]
  datastr = pool+' '+name+' '+size+' '+groups+' '+ipaddress+' '+Subnet+' disabled '+user+' '+owner+' '+user
 print('#############################')
 print('/TopStor/VolumeCreate'+typep,datastr)
 print('###########################')
 cmndstring = '/TopStor/VolumeCreate'+typep+' '+datastr
 result=subprocess.run(cmndstring.split(),stdout=subprocess.PIPE)
 return 


if __name__=='__main__':

 createvol(*sys.argv[1:])

