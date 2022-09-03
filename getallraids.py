#!/bin/python3.6

from allphysicalinfo import getall 
from etcdgetpy import etcdget as get
from levelthis import levelthis
from copy import deepcopy 

def selectnewmirror(fdisk, diskdict, fmirror):
 single = newraids(diskdict)['single']
 fmdisks = [x for x in fmirror['disks'] if x != fdisk]
 size = float('inf')
 fmhosts = set()
 for disk in fmdisks:
  size = min(diskdict[disk]['size'],size)
  fmhosts.add(diskdict[disk]['host'])
 group = len(fmdisks) + 1
 mirror = dict() 
 possizes = [x for x in single if float(x) >= float(size)]
 possizes.sort(reverse=True)
 hostdisks = dict()
 hosts = set()
 for syz in possizes:
  for dsk in single[syz]:
   if dsk == fdisk or dsk in fmdisks:
    continue
   if diskdict[dsk]['host'] not in hostdisks:
    hostdisks[diskdict[dsk]['host']] = []
   hostdisks[diskdict[dsk]['host']].append(dsk)
   hosts.add(diskdict[dsk]['host'])
 pool = fmirror['pool']
 balance = get('balance', pool)[0][1]
 hostdiskcopy = deepcopy(hostdisks)
 hosts = list(hosts)
 finishedhosts = set() 
 posdisks = []
 if 'Availability' in balance:
  notdone = 1 
  hostcount = len(hosts)
  while notdone:
   chost = hosts[(notdone-1) % hostcount] 
   if len(hostdiskcopy[chost]):
    cdisk = hostdiskcopy[chost].pop(); 
    notdone += 1
    if chost not in fmhosts:
     posdisks.append[cdisk]
   else:
    finishedhosts.add(chost)
   if len(finishedhosts) == hostcount: 
    notdone = 0
 if not len(posdisks) or 'Availability' not in balance:
  hostdiskcopy = deepcopy(hostdisks)
  notdone = 1 
  while notdone:
   chost = hosts[(notdone-1) % hostcount] 
   if len(hostdiskcopy[chost]):
    cdisk = hostdiskcopy[chost].pop(); 
    notdone += 1
    posdisks.append(cdisk)
   else:
    finishedhosts.add(chost)
   if len(finishedhosts) == hostcount: 
    notdone = 0

 if not len(posdisks):
  posdisks = 'Nodisk'
 return posdisks 


def getmirror(single,group,diskdict):
 mirror = dict() 
 for size in single:
  otherslist = [] 
  hosts = set()
  othershosts = set()
  posdiskc = 0
  for others in single:
   if others > size:
    posdiskc += len(single[others])
    otherslist.append(others)
    for dsk in single[others]:
     othershosts.add(diskdict[dsk]['host'])
  sizec = len(single[size])
  for dsk in single[size]:
   hosts.add(diskdict[dsk]['host'])
  if sizec > 0 and (posdiskc+sizec) >= group:
   mirror[size] = {'disk':size, 'diskcount':group, 'others':otherslist, 'hosts': list(hosts), 'othershosts': list(othershosts)} 
 return mirror

def getraid(single,group,parity,diskdict):
 theraid = dict()
 for size in single:
  otherslist = [] 
  hosts = set()
  othershosts = set()
  posdiskc = 0
  for others in single:
   if others > size:
    posdiskc += len(single[others])
    otherslist.append(others)
    for dsk in single[others]:
     othershosts.add(diskdict[dsk]['host'])
  dif = posdiskc + len(single[size]) - group
  for dsk in single[size]:
   hosts.add(diskdict[dsk]['host'])
  base = round(size*(group - parity ),2)
  count = 0 
  while dif >= 0:
   theraid[base] = {'disk':size, 'diskcount':group+count, 'others':otherslist, 'hosts': list(hosts), 'othershosts': list(othershosts)} 
   base += size
   dif -= 1 
   count += 1
 return theraid

allraids ={'raid5':{'parity':1, 'group':3 } , 'raid6':{ 'parity':2, 'group':4}, 'volset':{ 'parity':0, 'group':2},
           'raid6plus':{'parity':3, 'group':5} }

def newraids(diskdict):
 allsizes = dict() 
 single = dict() 
 allsizes['single'] = single
 for disk in diskdict:
  if 'free' in diskdict[disk]['raid']:
   if diskdict[disk]['size'] not in single:
    single[diskdict[disk]['size']] = []
   single[diskdict[disk]['size']].append(disk)
 for raid in allraids:
  theraid = getraid(single,allraids[raid]['group'],allraids[raid]['parity'],diskdict) 
  if len(theraid) > 0:
   allsizes[raid] = theraid.copy()
 theraid = getmirror(single,2,diskdict)
 if len(theraid) > 0:
  allsizes['mirror'] = theraid
 return allsizes

def selectdisks(disks,singles, disksinfo):
 #print('#########disks',disks)
 #print('#########singles',singles)
 thedisks = []
 others = disks['others']
 others.sort(reverse=True)
 diskgroups = others 
 diskgroups.append(disks['disk'] )
 diskcount = disks['diskcount']
 #print('---------diskcount',diskcount)
 while diskcount > 0:
  nextgroup = diskgroups.pop()
  hostdisks = dict()
  hosts = set()
  disks = singles[nextgroup] 
  #print('------------diskcount2,',diskcount)
  for dsk in disks:
   hosts.add(disksinfo[dsk]['host'])
   if disksinfo[dsk]['host'] not in hostdisks:
    hostdisks[disksinfo[dsk]['host']] = []
   hostdisks[disksinfo[dsk]['host']].append(dsk)
  #print('-----------hostdisks',hostdisks)
  diskc = min(diskcount, len(disks))
  hosts = list(hosts)
  hostcount = len(hosts)
  while diskc > 0:
   host = hosts[ diskc % hostcount ] 
   if len(hostdisks[host]) > 0:
    thedisks.append(hostdisks[host].pop()) 
    diskc -= 1
   else:
    hostcount -= 1
  diskcount -= len(disks)
 #print('thehththeheh',thedisks)
 return thedisks


if __name__=='__main__':
 alldsks = get('host','current')
 allinfo = getall(alldsks)
 disks = allinfo['disks']
 raids = newraids(disks)
 print(raids)
 
