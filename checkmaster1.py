#!/bin/python3.6
import os, time
start = time.time()
proc1 =  os.popen('pcs resource')
if ('mgmtip' in proc1.read()):
	print('Yes')
else: 
	print('No')
end = time.time()	
print((end - start) * 10 ** 9)
