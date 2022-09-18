#!/bin/python3.6
import subprocess,sys,os
def etcdget(key, prefix=''):
	proc = os.popen('netstat -ant | grep 2378')
	allLines = proc.read().splitlines()
	openCount = 0
	for line in allLines:
		lineSplitted = ' '.join(line.split()).split(' ')
		port = lineSplitted[3].split(':')[1]
		if (port == '2378'):
			openCount += 1
	if (openCount != 0):
		import etcdgetlocal
		proc2 = os.popen('pcs resource show CC')
		resources = "".join(proc2.read()).split('\n')
		ip = resources[1].split(" ")[4].split('=')[1]
		etcdgetlocal.etcdget(ip, key, prefix)
	else:
		import etcdget
		etcdget.etcdget(key, prefix)
	
if __name__=='__main__':
 etcdget(*sys.argv[1:])
