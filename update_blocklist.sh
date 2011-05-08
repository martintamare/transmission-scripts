#!/bin/sh

PID="`pidof transmission-daemon`"
if [ -n "$PID" ]; then
        kill $PID
fi

echo -n "Waiting for the daemon to exit "
sleep 2

COUNT=1
while [ -n "`pidof transmission-daemon`" ]; do
        COUNT=$((COUNT + 1))
        if [ $COUNT -gt 60 ]; then
                echo -n "transmission-daemon doesn't respond, killing it with -9"
                kill -9 `pidof transmission-daemon`
                break
        fi

        sleep 2
        echo -n "."
done

echo " done"

cd /var/lib/transmission-daemon/info/blocklists/
if wget http://www.bluetack.co.uk/config/level1.gz 1>/dev/null 2>&1 ; then
        rm -f level1 && gunzip level1.gz
        echo "blocklist updated"
else
        echo "blocklist not updated"
fi

/etc/init.d/transmission-daemon start
