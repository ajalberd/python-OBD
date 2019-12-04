import obd
import sys
import os
import time
#obd.logger.setLevel(obd.logging.DEBUG)

ports = obd.scan_serial()
print ports
connection = obd.OBD(fast=False, timeout=30) #, check_voltage=False) # auto-connects to USB or RF port

cmd = obd.commands.SPEED # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response

#print(response.value) # returns unit-bearing values thanks to Pint
#print(response.value.to("mph")) # user-friendly unit conversions
f = open("output.txt","w+")
while(True):
	time.sleep(0.8)
	rpm = connection.query(obd.commands.RPM).value.magnitude
	print(rpm)
	rpms= str(rpm)
	output = 'python3 display.py'
	output = output + ' ' + rpms
	os.system(output)
	
