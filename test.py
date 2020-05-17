import obd
import sys
import os
import time
import math
import subprocess
#obd.logger.setLevel(obd.logging.DEBUG)
from threading import *

ports = obd.scan_serial()
#print (ports)
connection = obd.OBD(fast=True, timeout=30, check_voltage=False) # auto-connects to USB or RF port

cmd = obd.commands.SPEED # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response

#print(response.value) # returns unit-bearing values thanks to Pint
#print(response.value.to("mph")) # user-friendly unit conversions
screen_lock = Semaphore(value=1)
speed = 0
rpm = 0
middle = ""
msg = ""

#rpmarr = [6786,5554,3334,6753,3256]
#speedarr = [20,30,40,60,80]

def speedandrpm():
    global speed
    global rpm
    while(True):
        time.sleep(0.2)
        screen_lock.acquire()
        try:
            rpm = int(connection.query(obd.commands.RPM).value.magnitude)
            print(rpm)
            speed = int(connection.query(cmd).value.magnitude)
        except:
            print('RPM, Speed read error')
        screen_lock.release()
        print(speed)

def voicerec():
    #time.sleep(10)
    global middle
    global msg
    while(True):
        msg = porcupineproc.stdout.readline().rstrip('\n')
        if msg == 'picovoice':
            print('picovoice detected')
            screen_lock.acquire()
            middle = str(connection.query(obd.commands.FUEL_LEVEL).value.magnitude)
            screen_lock.release()
        elif msg == 'porcupine':
            screen_lock.acquire()
            middle = str(connection.query(obd.commands.RUN_TIME).value.magnitude)
            screen_lock.release()
        #process.poll()
        print(middle)

def runGUI():
    time.sleep(20)
    global speed
    global rpm
    global middle
    while(True):
        time.sleep(.1)
        screen_lock.acquire()
        val = str(speed)+','+str(rpm) + ',' + middle + '\n'
        guiprocess.stdin.write(val)
        screen_lock.release()
        #print(val)

t1 = Thread(target = speedandrpm)
porcupineproc = subprocess.Popen(['python3', '../porcupine-pi/demo/python/porcupine_demo_mic.py', '--keywords=porcupine,picovoice','--input_audio_device_index', '3'], stdout=subprocess.PIPE, universal_newlines=True)
t2 = Thread(target = voicerec)
guiprocess = subprocess.Popen(['python3', '../SeniorDesignGUI/GUI.py'], stdin=subprocess.PIPE, bufsize=1, universal_newlines=True, cwd='../SeniorDesignGUI/')
t3 = Thread(target = runGUI)
t2.start()
t1.start()
t3.start()



#listener.close()



