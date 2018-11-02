#!/usr/bin/python

import argparse
import rrdtool
from subprocess import check_output
from re import findall
from time import sleep, strftime, time

databaseFile = "/run/temperature_log/temperature_log.rrd"

def get_temp_dht11():
    output = check_output(["sudo", "/usr/local/bin/dht11"]).decode("UTF-8")
    temp, humidity = findall("\d+\.?\d*",output)
    if args.verbose:
        print "DHT11 temperature is %s and humidity is %s" % (temp, humidity)
    return(temp,humidity)

def get_temp_rpi_internal():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.?\d*",temp)[0])
    if args.verbose:
        print "rPi internal temperature is %s" % temp
    return(temp)

def get_temp_temper_usb():
    temp = check_output(["/usr/local/bin/temper"]).decode("UTF-8")
    temp = float(findall("\d+\.?\d*",temp)[0])
    if args.verbose:
        print "USB TEMPer temperature is %s" % temp
    return(temp)

def get_temp_outside():
    temp = check_output(["/usr/local/bin/outside_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.?\d*",temp)[0])
    if args.verbose:
        print "Outside temperature is %s" % temp
    return(temp)

def update_all():
    template = ""
    update = "N:"

    template += "rpi:"
    update += "%f:" % get_temp_rpi_internal()

    template += "usbtemper:"
    update += "%f:" % get_temp_temper_usb()

    dht11_t, dht11_h = get_temp_dht11()
    template += "dht11temp:"
    update += "%f:" % float(dht11_t)
    template += "dht11hum:"
    update += "%f:" % float(dht11_h)

    out_temp = get_temp_outside()
    if out_temp:
        template += "outside:"
        update += "%f:" % out_temp

    update = update[:-1]
    template = template[:-1]
    if args.verbose > 1:
        print "DEBUG: rrdtool update %s --template %s %s" % (databaseFile, template, update)
    rrdtool.update(databaseFile, "--template", template, update)

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="count")
args = parser.parse_args()

update_all()
