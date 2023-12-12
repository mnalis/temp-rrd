#!/usr/bin/python

import argparse
import rrdtool
from subprocess import check_output
from re import findall
from time import sleep, strftime, time

databaseFile = "/run/temperature_log/temperature_log.rrd"

def get_temp_dht11():
    try:
        output = check_output(["sudo", "/usr/local/bin/dht11"]).decode("UTF-8")
        temp, humidity = findall("\d+\.?\d*",output)
        if args.verbose:
            print ("DHT11 temperature is %s and humidity is %s" % (temp, humidity))
        return(temp,humidity)
    except:
        if args.verbose:
            print ("DHT11 fetch failed, ignoring it")

def get_temp_rpi_internal():
    try:
        temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
        temp = float(findall("-?\d+\.?\d*",temp)[0])
        if args.verbose:
            print ("rPi internal temperature is %s" % temp)
        return(temp)
    except:
        if args.verbose:
            print ("rPi internal sensor fetch failed, ignoring it")

def get_temp_temper_usb():
    try:
        temp = check_output(["/usr/local/bin/temper"]).decode("UTF-8")
        temp = float(findall("-?\d+\.?\d*",temp)[0])
        if args.verbose:
            print ("USB TEMPer temperature is %s" % temp)
        return(temp)
    except:
        if args.verbose:
            print ("USB TEMPer fetch failed, ignoring it")

def get_temp_outside():
    try:
        temp = check_output(["/usr/local/bin/outside_temp"]).decode("UTF-8")
        temp = float(findall("-?\d+\.?\d*",temp)[0])
        if args.verbose:
            print ("Outside temperature is %s" % temp)
        return(temp)
    except:
        if args.verbose:
            print ("Outside temperature fetch failed, ignoring it")

def update_all():
    template = ""
    update = "N:"

    rpi_t = get_temp_rpi_internal()
    if rpi_t:
        template += "rpi:"
        update += "%f:" % rpi_t

    temper_t = get_temp_temper_usb()
    if temper_t:
        template += "usbtemper:"
        update += "%f:" % temper_t

    dht11_t, dht11_h = get_temp_dht11()
    if dht11_t:
        template += "dht11temp:"
        update += "%f:" % float(dht11_t)
    if dht11_h:
        template += "dht11hum:"
        update += "%f:" % float(dht11_h)

    out_temp = get_temp_outside()
    if out_temp:
        template += "outside:"
        update += "%f:" % out_temp

    update = update[:-1]
    template = template[:-1]
    if args.verbose > 1:
        print ("DEBUG: rrdtool update %s --template %s %s" % (databaseFile, template, update))
    rrdtool.update(databaseFile, "--template", template, update)

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="count")
args = parser.parse_args()

update_all()
