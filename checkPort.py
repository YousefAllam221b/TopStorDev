#!/bin/python3.6
import subprocess,sys, os
import socket
def checkPort(key, prefix=''):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	result = sock.connect_ex(('10.11.11.244',80))
	print(result)
	return result 

if __name__=='__main__':
 checkPort(*sys.argv[1:])
