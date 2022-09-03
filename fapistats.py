#!/bin/python3.6

from allphysicalinfo import getall 
from etcdgetpy import etcdget as get
from levelthis import levelthis

vollisting = ['used', 'quota', 'usedbysnapshots' ]

def volumes(voldict):
 global vollisting
 for vol in voldict:
  for vollist in vollisting:
   voldict[vol][vollist] = levelthis(voldict[vol][vollist])
 return voldict

def cpuperf():
 perfs = get('cpuperf', '--prefix')
 perfslst = []
 for perf in perfs:
  host = perf[0].replace('cpuperf/','')
  perfdict = {'host': host, 'cpu': perf[1] }
  perfslst.append(perfdict)

 return perfslst


def dskperf():
 perfs = get('dskperf','--prefix')
 perfslst = []
 for perf in perfs:
  host = perf[0].split('/')[1]
  diskname = perf[0].split('/')[2]
  dsk = perf[1].split('/')
  perfdict = { 'host':host, 'diskname':diskname, 'disklun':dsk[-1], 'tps':dsk[0], 
               'thr':dsk[1], 'readpercent':dsk[2]
             }
  perfslst.append(perfdict)
 return perfslst

def statsvol(voldict, limit=3):
 global vollisting
 statsdict = dict()
 statsdict['trends'] = {}
 for vollist in vollisting:
  pairing = []
  for vol in voldict:
   statsdict['trends'][vol] = get('sizevol/'+voldict[vol]['pool']+'/'+vol)[0]
   pairing.append([vol.split('_')[0], vol, voldict[vol][vollist]])
  pairing.sort(key=lambda x:x[2],reverse=True)
  finalpairing = []
  otherstats = 0
  count = -1
  for pair in pairing:
   count += 1
   if count < 3:
    finalpairing.append(pairing[count])
   else:
    otherstats += pairing[count][2]
  statsdict[vollist] = {'fulllabels':['others'], 'labels':['others'], 'stats':[otherstats] }
  for pair in finalpairing:
   statsdict[vollist]['fulllabels'].append(pair[1])
   statsdict[vollist]['labels'].append(pair[0])
   statsdict[vollist]['stats'].append(pair[2])
 return statsdict


def statsvol_all(voldict):
 global vollisting
 statsdict = dict()
 for vollist in vollisting:
  labels = []
  fulllabels = []
  stats = []
  for vol in voldict:
   labels.append(vol.split('_')[0])
   fulllabels.append(vol)
   stats.append(voldict[vol][vollist])
  statsdict[vollist] = {'fulllabels':list(fulllabels), 'labels':list(labels), 'stats':list(stats) }
 return statsdict 


def allvolstats(allinfo):
 vols = volumes(allinfo['volumes'])
 return statsvol(vols)
  

if __name__=='__main__':
 alldsks = get('host','current')
 allinfo = getall(alldsks)
 vols = volumes(allinfo['volumes'])
 #statsvol(vols)
 dskperf()
 
 
