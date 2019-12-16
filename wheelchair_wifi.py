####################################################################
####################################################################

## PROBABLEMENTE FUNCION INUTIL

####################################################################
####################################################################
# Imports
# WiFi
from openbci import cyton as board
# Cyton ?
# from openbci import OpenBCICyton
# Requests per a fer cridades al OpenBCI WiFi Server
import requests
import asyncore
import sys
import time

def handle_streamed_data(sample):
	print "espetetes1"
	print(sample.sample_number)
	print(sample.channel_data)
	print "espetetes2"

# Declarem 'main' function
if __name__ == '__main__':

# Parametres de la conexio
	ip_address = '192.168.4.1'
	shield_name = 'OpenBCI-79AB'
	sample_rate = 500
	log = True
	timeout = 5
	max_packets_to_skip = 10
	latency = 5000
	high_speed = False
	ssdp_attempts = 10

	# Intentem la conexio
	connection = board.OpenBCICyton(ip_address=ip_address,
					   shield_name=shield_name,
					   sample_rate=sample_rate,
					   log=log,
					   timeout=timeout,
					   max_packets_to_skip=max_packets_to_skip,
					   latency=latency,
					   high_speed=high_speed,
					   ssdp_attempts=ssdp_attempts)
	
	time.sleep(1)
	connection.connect()
	print("WiFi Shield Connected with board")   
	time.sleep(1)
	print("WiFi Shield streaming started...")   
	connection.start_streaming(handle_streamed_data)
	connection.loop()
	
	# Note: do this when you're finished streaming:
	connection.stop()
	connection.disconnect()





