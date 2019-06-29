#!/bin/bash
ping -c 1 -W 1 www.google.com
rc=$?
if [[ $rc -ne 0 ]] ; then
    echo "$(date) Not able to access internet - restarting"  >> /home/pi/wifi-check.log
    reboot
fi