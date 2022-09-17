#!/bin/python3.6
import traceback, hashlib
import subprocess
from ast import literal_eval as mtuple
from etcddel import etcddel as dels
from etcdput import etcdput as put 
import time 

nowis = int(time.time())
nowfixed = str(nowis)[:4]
cmdline='./grepthis.sh '+nowfixed+' /var/www/html/des20/Data/TopStorglobal.log'
result=subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
onedaylog = []
for res in result:
 if len(res.split()) < 4:
  continue
 if int(res.split()[-1]) > (nowis-3600):
  onedaylog.append(res)

