#!/usr/bin/python

import rrdtool
from subprocess import check_output
from re import findall
from time import sleep, strftime, time

databaseFile = "/run/temperature_log/temperature_log.rrd"

def get_temp_rpi_internal():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    return(temp)

def get_temp_temper_usb():
    temp = check_output(["/usr/local/bin/temper"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    return(temp)

def update_all():
    template = ""
    update = "N:"

    template += "rpi:"
    update += "%f:" % get_temp_rpi_internal()

    template += "usbtemper:"
    update += "%f:" % get_temp_temper_usb()

    update = update[:-1]
    template = template[:-1]
    rrdtool.update(databaseFile, "--template", template, update)

update_all()
