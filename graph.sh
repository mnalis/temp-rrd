#!/bin/sh

exec > /dev/null

COMMON='
  --width=640 --height=480 
  --lower-limit=-10 
  --step=60 -v degreesC 
  DEF:temp1=/run/temperature_log/temperature_log.rrd:rpi:AVERAGE 
  DEF:temp2=/run/temperature_log/temperature_log.rrd:usbtemper:AVERAGE 
  DEF:temp3=/run/temperature_log/temperature_log.rrd:outside:AVERAGE 
  DEF:temp4=/run/temperature_log/temperature_log.rrd:dht11temp:AVERAGE 
  DEF:humidity=/run/temperature_log/temperature_log.rrd:dht11hum:AVERAGE 
  LINE2:temp1#A00000:"rPi_internal" 
  LINE2:temp2#008000:"USB_TEMPer" 
  AREA:temp3#00008080:"Outside" 
  LINE2:temp4#60F000:"DHT11_temp" 
  LINE2:humidity#FFA500:"DHT11_humid" 
  HRULE:0#0000FF:"freezing" 
  HRULE:18#00FFFF:"cold"
'

rrdtool graph  /run/temperature_log/one_day.png \
  --title "Temperature (degrees C), 1 day" \
  --start now-1d --end now \
  $COMMON

rrdtool graph  /run/temperature_log/one_week.png \
  --title "Temperature (degrees C), 1 week" \
  --start now-7d --end now \
  $COMMON

rrdtool graph  /run/temperature_log/one_month.png \
  --title "Temperature (degrees C), 1 month" \
  --start now-30d --end now \
  $COMMON

rrdtool graph  /run/temperature_log/one_year.png \
  --title "Temperature (degrees C), 1 year" \
  --start now-365d --end now \
  $COMMON

