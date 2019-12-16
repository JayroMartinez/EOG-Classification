from openbci import cyton as board
import time
from datetime import datetime
import random
from pydub import AudioSegment
from pydub.playback import play
from sys import exit as exit
import platform
from sklearn.svm import SVC
import numpy as np
import platform
import pickle
from multiprocessing import Process
import glob

import filter_files as filt
import feature_extraction as feat
import global_variables


# Lists to store the horizontal and vertical components of the online data
online_data_hor = []
online_data_ver = []

# Counter for number of datapoints acquired
cont = global_variables.get_cont()


def custom_append(lst, item):
	"""
FUNCTION:		custom_append(self, item)
INPUT:			The list where to append and the item to append
OUTPUT:			None
DESCRIPTION:	This function appends an element to a list removing the 
				elements that exceeds the maximum size
	"""

	samples_per_trial = global_variables.get_samples_per_trial()
	
	lst.append(item)
	if len(lst)>samples_per_trial:
		lst[:1]=[]
				
				

def connect():
	"""
FUNCTION:		connect()
INPUT:			None
OUTPUT:			Call to acquire(connection)
DESCRIPTION:	Creates the connection with OpenBCI Cyton Board,
				sets the configuration & calls to acquire function
	"""
	
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

	acquire(connection)
	

def acquire(connection):
	"""
# FUNCTION:	 	acquire(connection)
# INPUT: 		connection object
# OUTPUT: 		Loop over handle_streamed_data
# DESCRIPTION:	Streams the data from Cyton Board
	"""

	#print("Dongle Connected with board")   
	time.sleep(1)
	#print("Dongle streaming started...")

	#connection.print_register_settings()  
	connection.start_streaming(handle_streamed_data)
	connection.loop()


def online_calculations(online_data_hor, online_data_ver):

	samples_per_trial = global_variables.get_samples_per_trial()
	lab = global_variables.get_lab()
	model_name = global_variables.get_model()
	model = pickle.load(open(model_name, 'rb'))

# Pre-processing
	filtered_hor = filt.online_filter(online_data_hor)
	filtered_ver = filt.online_filter(online_data_ver)
	
# Feature Extraction
	features = feat.features([filtered_hor], [filtered_ver])

# Check if there's a movement or not
	probs = model.predict_proba(features)
	
	lab.sort()
	max_pos = int(np.where(probs[0] == np.max(probs[0]))[0])
	movement = lab[max_pos]
	
	print("\n********************************************")
	
	if np.max(probs) > 0.5:
		print(lab)
		print(np.max(probs))
		print("MOVEMENT DETECTED: ", movement)

	file_name = global_variables.get_online_data_file()
	new_file_name = "./data/"+file_name+".txt"
	file = open(new_file_name, 'a')
	str_write = str([online_data_hor,online_data_ver])+"\n"
	file.write(str_write)
	file.close()



def handle_streamed_data(sample):
	"""
# FUNCTION:	 	handle_streamed_data(sample)
# INPUT: 		Sample object
# OUTPUT: 		None
# DESCRIPTION:	Reads the data and saves it on a .txt file,
#				also plays audio files with actions when its necessary
	"""

	global online_data_hor,online_data_ver, cont
	
	cont = global_variables.get_cont()
	samples_per_trial = global_variables.get_samples_per_trial()
	evaluation_time = global_variables.get_evaluation_time()
	sample_rate = global_variables.get_sample_rate()
	lab = global_variables.get_lab()
	
# If we are before first seconds or not exactly every half second
	if (cont<samples_per_trial or cont%(sample_rate*evaluation_time) != 0):
		custom_append(online_data_hor, sample.channel_data[1])
		custom_append(online_data_ver, sample.channel_data[6])
		global_variables.set_cont(cont + 1)
# Every half second we evaluate the data
	else:

		new_process = Process(target=online_calculations, args=(online_data_hor, online_data_ver,))
		new_process.start()
		
		custom_append(online_data_hor, sample.channel_data[1])
		custom_append(online_data_ver, sample.channel_data[6])
		global_variables.set_cont(cont + 1)

			

def online_classif():
	"""
# FUNCTION:	 	online_classif(model)
# INPUT: 		Model used to predict the labels of the online acquired data
# OUTPUT: 		None
# DESCRIPTION:	This function acquires, pre-processes and extracts the features of the data in real time
#				and gives us the predicted label using the model previously trained
	"""	
	global play_labels, play_times
	
	model_name = global_variables.get_model()
	file_name = model_name.replace('.sav','_online_data')
	pos = file_name.find("/models/")
	file_name = file_name.replace(file_name[0:pos+len("/models/")],"")
	online_files = glob.glob("./data/"+file_name+"*")
	number_online_files = len(online_files)
	online_data_file_name = file_name+"_"+str(number_online_files+1)
	global_variables.set_online_data_file(online_data_file_name)
	file = open(online_data_file_name, 'w')
	file.close()

# Establish connection with OpenBCI board
	connect()
	
