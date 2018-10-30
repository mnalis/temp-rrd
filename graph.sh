#!/bin/sh

exec > /dev/null

#  --rigid

COMMON='
  --width=640 --height=480 
  --lower-limit=-10 
  --upper-limit=50
  --step=60
  --vertical-label degrees_Celsius
  --right-axis-label %relative_humidity
  --right-axis 2:0
  --slope-mode
  --alt-y-grid 
  DEF:temp1=/run/temperature_log/temperature_log.rrd:rpi:AVERAGE 
  DEF:temp2=/run/temperature_log/temperature_log.rrd:usbtemper:AVERAGE 
  DEF:temp3=/run/temperature_log/temperature_log.rrd:outside:AVERAGE 
  DEF:temp4=/run/temperature_log/temperature_log.rrd:dht11temp:AVERAGE 
  DEF:humidity=/run/temperature_log/temperature_log.rrd:dht11hum:AVERAGE 
  CDEF:scaled_humidity=humidity,2,/
  LINE2:temp1#A00000:"rPi_internal" 
  LINE2:temp2#008000:"USB_TEMPer" 
  AREA:temp3#00008080:"Outside" 
  LINE2:temp4#60F000:"DHT11_temp" 
  LINE2:scaled_humidity#FFA500:"DHT11_humid":dashes
  HRULE:0#0000FF:"freezing" 
  HRULE:18#00FFFF:"cold"
  GPRINT:humidity:LAST:Current_Humidity\:%3.0lf%%
  GPRINT:temp4:LAST:Current_IN\:%3.0lfC
  GPRINT:temp3:LAST:Current_OUT\:%3.0lfC
'

rrdtool graph  /run/temperature_log/one_day.png \
  --title "Temperature (degrees C), 1 day" \
  --watermark "`date`" \
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

