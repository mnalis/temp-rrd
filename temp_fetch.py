#!/usr/bin/python

import argparse
import rrdtool
from subprocess import check_output
from re import findall
from time import sleep, strftime, time

databaseFile = "/run/temperature_log/temperature_log.rrd"

def get_temp_dht11():
    output = check_output(["sudo", "/usr/local/bin/dht11"]).decode("UTF-8")
    temp, humidity = findall("\d+\.\d+",output)
    if args.verbose:
        print "DHT11 temperature is %s and humidity is %s" % (temp, humidity)
    return(temp,humidity)

def get_temp_rpi_internal():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    if args.verbose:
        print "rPi internal temperature is %s" % temp
    return(temp)

def get_temp_temper_usb():
    temp = check_output(["/usr/local/bin/temper"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    if args.verbose:
        print "USB TEMPer temperature is %s" % temp
    return(temp)

def get_temp_outside():
    import urllib2
    import json

    try:
        f = urllib2.urlopen('https://api.openweathermap.org/data/2.5/weather?APPID=' + args.apikey + '&units=metric&' + args.apiloc)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        temp = parsed_json['main']['temp']
        if args.verbose:
            location = parsed_json['name']
            print "Current outside temperature at %s (specified %s) is: %s" % (location, args.apiloc, temp)
        f.close()
        return(temp)
    except:
        return


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

    if args.apikey:
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
parser.add_argument("--apikey", help="openweathermap.org API key, register to get one")
parser.add_argument("--apiloc", help="openweathermap.org locator from https://openweathermap.org/current, like 'q=London,uk' or 'lat=45.80303&lon=15.92889'")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="count")
args = parser.parse_args()

update_all()
