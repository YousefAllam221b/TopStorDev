#!/bin/sh
echo $@ > /root/receivekeys
partner=`echo $@ | awk '{print $1}'`
partnerip=`echo $@ | awk '{print $2}'`
clusterip=`echo $@ | awk '{print $3}'`
ptype=`echo $@ | awk '{print $4}'`
port=`echo $@ | awk '{print $5}'`
ppass=`echo $@ | awk '{print $6}'`
keys=`echo $@ | awk '{print $7}'`
./etcdget.py Partner $clusterip | grep $ppass | grep $port 
if [ $? -eq 0 ];
then
 echo it is okok >> /root/receivekeys
 myip=`/sbin/pcs resource show CC | grep Attrib | awk -F'ip=' '{print $2}' | awk '{print $1}'` 
 ./etcdput.py nodesender/${clusterip}/$partnerip/$myip $partner
 ./etcdputlocal.py $myip nodesender/${clusterip}/$partnerip $partner   2>/dev/null
 authkeys=`cat /root/.ssh/authorized_keys | grep -v $partner`
 echo $authkeys > /root/.ssh/authorized_keys
 echo $keys | sed 's/\_spc\_/ /g' >> /root/.ssh/authorized_keys
 sshd=`cat /etc/ssh/sshd_config | grep -v "Port 22" | grep -v $port`
 echo -e "$sshd" > /etc/ssh/sshd_config
 echo -e "Port $port \r"  >> /etc/ssh/sshd_config
 echo -e "Port 22 \r" >> /etc/ssh/sshd_config
 systemctl restart sshd
 chmod 004 /root/.ssh/authorized_keys
fi
