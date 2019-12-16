####################################################################
####################################################################

## PROBABLEMENTE FUNCION INUTIL

####################################################################
####################################################################
# Imports
# WiFi
from openbci import cyton as board
from openbci.plugins import csv_collect as csv
from pydub import AudioSegment
from pydub.playback import play
import random
# Cyton ?
# from openbci import OpenBCICyton
# Requests per a fer cridades al OpenBCI WiFi Server
import requests
import asyncore
import sys
import time

iter = "global"
cont = "global"
#exit = "global"	

def handle_streamed_data(sample):
	#print(sample.sample_number)
	#print(sample.channel_data)
	#print(sample.aux_data)
	#print(sample.id)

	global iter
	global cont
	#global exit
	

	tmp_lab = labels[iter]

	if cont == 0:
		if tmp_lab == 'EXIT':
			file.close()
			connection.stop()
			connection.disconnect()
			print("**********************************")
			print("**********************************")
			print("**   TRAINNING BLOCK FINISHED   **")
			print("**********************************")
			print("**********************************")
			time.sleep(1)
			exit()
			#exit = True
		else:
			song_name = "./audio/"+tmp_lab+".mp3"
			song = AudioSegment.from_mp3(song_name)
			play(song)
			cont += 1
			sample.channel_data.insert(0,tmp_lab)
			str_chn_dta =  ' '.join([str(sample.channel_data)])
			file.write(str_chn_dta)
			file.write('\n')

	elif cont < 749:
		cont += 1
		sample.channel_data.insert(0,tmp_lab)
		str_chn_dta =  ' '.join([str(sample.channel_data)])
		file.write(str_chn_dta)
		file.write('\n')
	else:
		cont = 0
		iter +=1
		sample.channel_data.insert(0,tmp_lab)
		str_chn_dta =  ' '.join([str(sample.channel_data)])
		file.write(str_chn_dta)
		file.write('\n')

	#print(tmp_lab)

	

# Play 'audio.wav'
	# song = "/audio/audio.wav"
	# play(song)

# Write Data
	#str_chn_dta = ' '.join([str(sample.channel_data)]) 
	#file.write(float(str_chn_dta))
# Add label
	#sample.channel_data.insert(0,float(sample.timestamp))
	#file.write('\n')
	
# Declarem 'main' function
if __name__ == '__main__':

# Parametres de la conexio
	port = '/dev/tty.usbserial-DM01HL5T'
	baud = 115200
	filter_data = False
	scaled_output = True
	daisy = False
	aux = False
	impedance = False
	log = False
	timeout = None

# Obrim el fitxer 
	file = open("Bloque_10.txt", 'w')
	#print(file)
# Create labels, random shuffle & insert 5 beeps at the beginning
	lab = ['Up', 'Down', 'Left', 'Right']
	labels = lab*15
	random.shuffle(labels)
	for i in range(0,5):
		labels.insert(0,"beep")
	labels.append('EXIT')

# Create a counter
	cont = 0
# Create a boolean for exit
	#exit = False
# Create an iterator over labels list
	iter = 0

# Intentem la conexio
	connection = board.OpenBCICyton(port=port,
									baud=baud,
									filter_data=filter_data,
									scaled_output=scaled_output,
									daisy=daisy,
									aux=aux,
									impedance=impedance,
									log=log,
									timeout=timeout)
	
	time.sleep(1)
	connection.ser.write(b'1')
	connection.ser.write(b'3')
	connection.ser.write(b'4')
	connection.ser.write(b'5')
	connection.ser.write(b'6')
	connection.ser.write(b'8')
	connection.ser.write(b'x2040000X')
	connection.ser.write(b'x7040000X')
	#connection.connect()
	print("Dongle Connected with board")   
	time.sleep(1)
	print("Dongle streaming started...")
	connection.print_register_settings()  
	connection.start_streaming(handle_streamed_data)
	#while exit == False:
	connection.loop()
	
# Note: do this when you're finished streaming:
	#file.close()
	#connection.stop()
	#connection.disconnect()
	#print("**********************************")
	#print("**********************************")
	#print("**   TRAINNING BLOCK FINISHED   **")
	#print("**********************************")
	#print("**********************************")
	#time.sleep(1)
	#exit()






