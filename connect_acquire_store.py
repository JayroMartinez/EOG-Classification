#	HERE WE CREATE THE CONNECTION WITH THE OPENBCI DEVICE AND WE HANDLE THE ACQUIRED DATA
#	AUTHOR: Jayro Martinez Cervero

from openbci import cyton as board
import time
import random
from pydub import AudioSegment
from pydub.playback import play
from sys import exit as exit
import platform
from multiprocessing import Process

import global_variables
from terminal_menu import menu

global iter, cont, connection

iter = global_variables.get_iter()
cont = global_variables.get_cont()


def connect():
	"""
# FUNCTION:		connect()
# INPUT:		None
# OUTPUT:		Call to acquire_save(connect)
# DESCRIPTION:	Creates the connection with OpenBCI Cyton Board
				and sets the configuration
# AUTHOR:		Jayro Martinez-Cervero
	"""

	global connection

# CONNECTION PARAMETERS
	# Check for OS system
	if platform.system() == 'Darwin':	# Mac OSX
		port = '/dev/tty.usbserial-DM01HL5T'
	else:								# Raspberry Pi
		port = '/dev/ttyUSB0'

	baud = 115200
	filter_data = False
	scaled_output = True
	daisy = False
	aux = False
	impedance = False
	log = False
	timeout = None

# CONNECTION ESTABLISHMENT
	connection = board.OpenBCICyton(port=port,
									baud=baud,
									filter_data=filter_data,
									scaled_output=scaled_output,
									daisy=daisy,
									aux=aux,
									impedance=impedance,
									log=log,
									timeout=timeout)

# CONFIGURATION
	time.sleep(1)
	# Turn Off channels [1, 3, 4, 5, 6, 8]
	connection.ser.write(b'1')
	connection.ser.write(b'3')
	connection.ser.write(b'4')
	connection.ser.write(b'5')
	connection.ser.write(b'6')
	connection.ser.write(b'8')
	# For channels 2 & 7: 
	# Power 'On'
	# Gain set to 'x8'
	# Input type to 'normal'
	# 'Remove' channel from bias
	# 'disconnect' channel from SRB2
	# 'disconnect' all channels from SRB1
	time.sleep(1)
	connection.ser.write(b'x2040000X')
	time.sleep(1)
	connection.ser.write(b'x7040000X')
	time.sleep(1)

	acquire_save()


def acquire_save():
	"""
# FUNCTION:	 	acquire_save(connection)
# INPUT: 		connection object
# OUTPUT: 		Loop over handle_streamed_data
# DESCRIPTION:	Streams the data from Cyton Board
# AUTHOR:		Jayro Martinez-Cervero
	"""

	global connection

	print("Dongle Connected with board")   
	time.sleep(1)
	print("Dongle streaming started...")

	connection.print_register_settings()  
	
	try:
		connection.start_streaming(handle_streamed_data)
		connection.loop()
	except:
		print("Connection closed")
		return


def stop_disconnect():
	"""
# FUNCTION:	 	stop_disconnect(connection)
# INPUT: 		connection object
# OUTPUT: 		None
# DESCRIPTION:	Stops the stream and disconnects the device
# AUTHOR:		Jayro Martinez-Cervero
	"""

	global connection

	connection.stop()
	connection.disconnect()
	

def play_sound(label): # FOR SOME REASON I DON'T REMEMBER, THIS FUNCTION IS NOT USED
	"""
# FUNCTION:	 	play_sound(label)
# INPUT: 		String with the movement label
# OUTPUT: 		None
# DESCRIPTION:	Reproduces the audio files
# AUTHOR:		Jayro Martinez-Cervero
	"""

	audio = AudioSegment.from_mp3("./audio/"+label+".mp3")
	play(audio)
	if label != 'beep':
				beep = AudioSegment.from_mp3("./audio/beep.mp3")
				play(beep)


def handle_streamed_data(sample):
	"""
# FUNCTION:	 	handle_streamed_data(sample)
# INPUT: 		Sample object
# OUTPUT: 		None
# DESCRIPTION:	Reads the data and saves it on a .txt file,
#				also plays audio files with actions when its necessary
# AUTHOR:		Jayro Martinez-Cervero
	"""

	labels = global_variables.get_labels()
	filename = global_variables.get_save_file()
	samples_per_trial = global_variables.get_samples_per_trial()

	global iter, cont

	tmp_lab = labels[iter]

	# Open file were we are going to save the data
	file = open(filename, 'a')

	if cont == 0:	# FIRST SAMPLE IN A TRIAL

		if tmp_lab == 'EXIT': # BLOCK FINISHED
			file.close()
			print("**********************************")
			print("**********************************")
			print("**   TRAINNING BLOCK FINISHED   **")
			print("**********************************")
			print("**********************************")
			cont = 0
			iter = 0
			global_variables.reset_labels()
			time.sleep(3)
			if not global_variables.get_interface():
				menu()
			else:
				stop_disconnect()
		else:
			audio = AudioSegment.from_mp3("./audio/"+tmp_lab+".mp3")
			play(audio)
			if tmp_lab != 'beep':
				beep = AudioSegment.from_mp3("./audio/beep.mp3")
				play(beep)
			
			cont+=1
			sample.channel_data.insert(0,tmp_lab)
			str_chn_dta =  ' '.join([str(sample.channel_data)])
			file.write(str_chn_dta)
			file.write('\n')
			

	elif cont < samples_per_trial-1:
		cont+=1
		sample.channel_data.insert(0,tmp_lab)
		str_chn_dta =  ' '.join([str(sample.channel_data)])
		file.write(str_chn_dta)
		file.write('\n')
	
	else:	# LAST SAMPLE IN A TRIAL
		cont = 0
		iter += 1
		sample.channel_data.insert(0,tmp_lab)
		str_chn_dta =  ' '.join([str(sample.channel_data)])
		file.write(str_chn_dta)
		file.write('\n')
	


