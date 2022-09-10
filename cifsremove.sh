#!/bin/sh
cd /TopStor
export ETCDCTL_API=3
enpdev='enp0s8'
pool=`echo $@ | awk '{print $1}'`
vol=`echo $@ | awk '{print $2}'`
volip=`echo $@ | awk '{print $3}'`
vtype=`echo $@ | awk '{print $4}'`
echo $@ > /root/`basename "$0"`
myhost=`hostname -s`
/TopStor/logqueue.py `basename "$0"` running $userreq
/TopStor/etcddel.py vol $vol
/TopStor/etcddel.py replivol $vol
/TopStor/etcddel.py size $vol 
/TopStor/deltolocal.py size $vol 
/TopStor/deltolocal.py vol $vol 
/TopStor/crondelete $vol
rm -rf /TopStordata/smb.${volip}.new
echo vol = $vol
/TopStor/delblock.py start${vol}_only stop${vol}_only /TopStordata/smb.$volip  ;
rm -rf /TopStordata/smb.$vol
rm -rf /$pool/smb.$vol
rm -rf /TopStordata/tempsmb.$volip
rm -rf /TopStordata/smb.$volip
cat /TopStordata/smb.${volip}.new
cat /TopStordata/smb.${volip}.new > /TopStordata/smb.${volip}
resname=$vtype'-'$volip
docker stop $resname
docker container rm $resname 
cat /TopStordata/smb.$volip | grep start | grep only
if [ $? -ne 0 ]
then 
  /sbin/pcs resource delete --force $resname  2>/dev/null
  rm -rf /TopStordata/smb.$volip;
else
 mounts=`cat /TopStordata/smb.$volip | grep '\[' | sed 's/\[//g' | sed 's/\]//g' | sed ':a;N;$!ba;s/\n/,/g'`
 echo mounts=$mounts
 mount=''
 for x in $mounts; 
 do
  mount=$mount'-v /'$pool'/'$x':/'$pool'/'$x':rw '
 done
 cp /TopStor/VolumeCIFSupdate.sh /etc/
 dockers=`docker ps -a`
 echo $dockers | grep $resname
 if [ $? -eq 0 ];
 then
  docker stop $resname 
  docker rm -f $resname
 fi
 docker run -d $mount --privileged \
  -e "HOSTIP=$ipaddr"  \
  -p $ipaddr:135:135 \
  -p $ipaddr:137-138:137-138/udp \
  -p $ipaddr:139:139 \
  -p $ipaddr:445:445 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /TopStordata/smb.${ipaddr}:/config/smb.conf:rw \
  -v /etc/:/hostetc/   \
  -v /var/lib/samba/private:/var/lib/samba/private:rw \
  --name $resname 10.11.11.124:5000/smb
  sleep 3
  docker exec $resname sh /hostetc/VolumeCIFSupdate.sh
  /TopStor/logqueue.py `basename "$0"` stop $userreq
fi
/TopStor/etcddel.py vol $vol
/TopStor/etcddel.py replivol $vol
/TopStor/logqueue.py `basename "$0"` finish $userreq
