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
  DEF:temp_rpi=/run/temperature_log/temperature_log.rrd:rpi:AVERAGE 
  DEF:temp_usb=/run/temperature_log/temperature_log.rrd:usbtemper:AVERAGE 
  DEF:temp_out=/run/temperature_log/temperature_log.rrd:outside:AVERAGE 
  DEF:temp_dht=/run/temperature_log/temperature_log.rrd:dht11temp:AVERAGE 
  DEF:humidity=/run/temperature_log/temperature_log.rrd:dht11hum:AVERAGE 
  CDEF:scaled_humidity=humidity,2,/

  HRULE:0#0000FF:freezing
  HRULE:18#00FFFF:cold

  LINE2:temp_rpi#A00000:rPi_internal
  LINE2:temp_usb#008000:USB_TEMPer

  COMMENT:\n

   AREA:temp_out#00008080:Outside\t
  GPRINT:temp_out:LAST:Last\:%3.0lfC
  GPRINT:temp_out:MIN:Min\:%3.0lfC
  GPRINT:temp_out:AVERAGE:Avg\:%3.0lfC
  GPRINT:temp_out:MAX:Max\:%3.0lfC\n

   LINE2:temp_dht#60F000:DHT11_temp\t
  GPRINT:temp_dht:LAST:Last\:%3.0lfC
  GPRINT:temp_dht:MIN:Min\:%3.0lfC
  GPRINT:temp_dht:AVERAGE:Avg\:%3.0lfC
  GPRINT:temp_dht:MAX:Max\:%3.0lfC\n
  
   LINE2:scaled_humidity#FFA500:DHT11_humid\t:dashes
  GPRINT:humidity:LAST:Last\:%3.0lf%%
  GPRINT:humidity:MIN:Min\:%3.0lf%%
  GPRINT:humidity:AVERAGE:Avg\:%3.0lf%%
  GPRINT:humidity:MAX:Max\:%3.0lf%%\n
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

