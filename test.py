import obd
import sys
import os
import time
#obd.logger.setLevel(obd.logging.DEBUG)
from multiprocessing.connection import Listener

address = ('127.0.0.1', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address)
conn = listener.accept()
print("listener accepted")

from threading import *

ports = obd.scan_serial()
print (ports)
connection = obd.OBD(fast=True, timeout=30, check_voltage=False) # auto-connects to USB or RF port

cmd = obd.commands.SPEED # select an OBD command (sensor)

#response = connection.query(cmd) # send the command, and parse the response

#print(response.value) # returns unit-bearing values thanks to Pint
#print(response.value.to("mph")) # user-friendly unit conversions
screen_lock = Semaphore(value=1)

def speedandrpm():
	while(True):
		time.sleep(0.8)
		screen_lock.acquire()
		rpm = connection.query(obd.commands.RPM).value.magnitude
		print(rpm)
		speed = connection.query(cmd)
		screen_lock.release()
		print(speed)
def voicerec():
	while(True):
		msg = conn.recv() #Recieve the message from porcupine...
		if msg == 'picovoice':
			print("Fuel level is: " + str(connection.query(obd.commands.FUEL_LEVEL).value))
			#break
		elif msg == 'porcupine':
			print("Runtime is: " + str(connection.query(obd.commands.RUN_TIME).value))
			#break
		#listener.close()
	#rpms= str(rpm)
	#rpms = reverse(rpms)
	#output = 'python3 display.py'
	#output = output + ' ' + rpms
	#os.system(output)


t1 = Thread(target = speedandrpm)
t2 = Thread(target = voicerec)

t1.start()
t2.start()



listener.close()
