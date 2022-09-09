#!/bin/python3.6
import subprocess,sys,os
def etcdget(key, prefix=''):
	if(prefix == '--prefix'):
		proc1 = os.popen('netstat -ant | grep 2378 | wc -l')
		wc_output = int(proc1.read())
		if (wc_output != 0):
			import etcdgetlocal
			print('Port 2378 is Open. Running ./etcdgetlocal.py')
			proc2 = os.popen('pcs resource show CC')
			resources = "".join(proc2.read()).split('\n')
			ip = resources[1].split(" ")[4].split('=')[1]
			etcdgetlocal.etcdget(ip, key, prefix)
		else:
			import etcdget
			print('Port 2378 is closed. Running ./etcdget.py')
			etcdget.etcdget(key, prefix)
	
if __name__=='__main__':
 etcdget(*sys.argv[1:])
