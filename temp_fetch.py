from subprocess import check_output
from re import findall
from time import sleep, strftime, time

def get_temp_rpi_internal():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    return(temp)

def get_temp_temper_usb():
    temp = check_output(["/usr/local/bin/temper"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    return(temp)

with open("cpu_temp.csv", "a") as log:
    while True:
        temp1 = get_temp_rpi_internal()
        temp2 = get_temp_temper_usb()
        log.write ("{0},{1},{2}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp1),str(temp2)))
        sleep(1)
