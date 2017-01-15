#!/usr/bin/python

import argparse
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

def get_temp_outside():
    import urllib2
    import json
    f = urllib2.urlopen('http://api.wunderground.com/api/' + args.apikey + '/geolookup/conditions/q/pws:' + args.apiid + '.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    #location = parsed_json['location']['city']
    temp = parsed_json['current_observation']['temp_c']
    #print "Current temperature in %s is: %s" % (location, temp_c)
    f.close()
    return(temp)


def update_all():
    template = ""
    update = "N:"

    template += "rpi:"
    update += "%f:" % get_temp_rpi_internal()
    template += "usbtemper:"
    update += "%f:" % get_temp_temper_usb()

    if args.apikey:
        template += "outside:"
        update += "%f:" % get_temp_outside()

    update = update[:-1]
    template = template[:-1]
    #print "DEBUG: rrdtool update %s --template %s %s" % (databaseFile, template, update)
    rrdtool.update(databaseFile, "--template", template, update)

parser = argparse.ArgumentParser()
parser.add_argument("--apikey", help="wunderground.com API key, register to get one")
parser.add_argument("--apiid", help="wunderground.com location ID, like IGRADZAG10")
args = parser.parse_args()

update_all()
