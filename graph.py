#!/bin/sh

rrdtool graph /var/www/html/temperature/one_day.png \
  --title "Temperature (degrees C), 1d" \
  --start now-1d --end now \
  --width=640 --height=480 \
  --step=60 -v degreesC \
  DEF:temp1=/run/temperature_log/temperature_log.rrd:rpi:AVERAGE \
  DEF:temp2=/run/temperature_log/temperature_log.rrd:usbtemper:AVERAGE \
  LINE2:temp1#008000:"rPi internal" \
  LINE2:temp2#800000:"USB TEMPer" \
  HRULE:0#0000FF:"freezing"
