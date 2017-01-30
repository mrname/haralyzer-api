#!/bin/sh
while $(curl http://$MYSQL_PORT_3306_TCP_ADDR:3306 > /dev/null 2>&1; [ "$?" -ne "0" ]); do sleep 3; echo "watiting for mysql to boot"; done
/usr/local/bin/python /pipeline/source/manage.py db migrate && /usr/local/bin/python /pipeline/source/manage.py runserver -h 0.0.0.0
