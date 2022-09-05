#!/bin/python3.6
import subprocess,sys

def etcdget(key, prefix=''):
	if(prefix == '--prefix'):
		netstat = ['netstat','-ant']
		grepPort= ['grep',':2378']
		countGrep= ['wc','-l']
		proc1 = subprocess.Popen(netstat,stdout=subprocess.PIPE)
		proc2 = subprocess.Popen(grepPort,stdin=proc1.stdout,stdout=subprocess.PIPE)
		proc3 = subprocess.Popen(countGrep,stdin=proc2.stdout,stdout=subprocess.PIPE)
		out=proc3.communicate()
		out = str(out)[3:][:-10]
		if (int(out) != 0):
			print('Port 2378 is Open. Running ./etcdgetlocal.py')
			getResources=['pcs','resource','show','CC']
			proc4 = subprocess.run(getResources,stdout=subprocess.PIPE)
			resources=proc4.stdout.decode('utf-8')
			resources = "".join(resources).split('\n')
			resourcesAttributes = resources[1]
			attributes= resourcesAttributes.split(" ")
			ip=attributes[4]
			ip=ip.split('=')[1]
			etcdgetlocal=['./etcdgetlocal.py',ip,'leader','--prefix']
			finalProc = subprocess.run(etcdgetlocal,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			print(finalProc)
		else:
			print('Port 2378 is closed. Running ./etcdget.py')
			etcdget=['./etcdget.py','leader','--prefix']
			finalProc=subprocess.run(etcdget,stdout=subprocess.PIPE)
			print(finalProc.stdout)

	
if __name__=='__main__':
 etcdget(*sys.argv[1:])
