#/bin/sh
x=`echo $@ | awk '{print $1}'`
username=`echo $@ | awk '{print $2}'`
userpass=`echo $@ | awk '{print $3}'`
/bin/smbpasswd -$x $username
( echo $userpass; echo $userpass) | /bin/smbpasswd -s -a $username 
