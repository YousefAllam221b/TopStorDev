#!/bin/sh
cd /TopStor
rm -rf key/adminfixed.gpg && cp factory/adminfixed.gpg key/adminfixed.gpg
newadmin=`cat /TopStor/factory/adminfixed.gpg`
./etcdput.py usershash/admin $newadmin
./etcddel.py usershashadm/admin --prefix
/TopStor/autoGenPatch
