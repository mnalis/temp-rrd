#!/bin/sh

rrdtool graph /var/www/html/temperature/one_day.png \
  --title "Temperature (degrees C), 1d" \
  --start now-1d --end now \
  --width=640 --height=480 \
  --step=60 -v degreesC \
  DEF:temp1=/run/temperature_log/temperature_log.rrd:rpi:AVERAGE \
  DEF:temp2=/run/temperature_log/temperature_log.rrd:usbtemper:AVERAGE \
  DEF:temp3=/run/temperature_log/temperature_log.rrd:outside:AVERAGE \
  LINE2:temp1#A00000:"rPi internal" \
  LINE2:temp2#008000:"USB TEMPer" \
  AREA:temp3#000080:"Outside" \
  HRULE:0#0000FF:"freezing"
  HRULE:18#00FFFF:"cold"

