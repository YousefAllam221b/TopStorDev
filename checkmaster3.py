#!/bin/python3.6
import os, time
proc1 = os.popen('pcs resource show CC')
resources = "".join(proc1.read()).split('\n')
ip = resources[1].split(" ")[4].split('=')[1]
start = time.time()
proc2 = os.popen('nmap '+ ip)
output = proc2.read()
end = time.time()
print((end - start) * 10 ** 9)
