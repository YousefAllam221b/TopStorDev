#!/bin/sh
cd /TopStor
newadmin=`cat /TopStor/factory/factoryadmin`
#./etcdput.py usershash/admin $newadmin
./etcdput.py usershashadm/admin $newadmin
