import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter

import read_function as read
import split_into_trials as tri
import global_variables


def filter():
	"""
# FUNCTION:	 	filter()
# INPUT: 		None
# OUTPUT: 		Vertical & horizontal components of the data divided by trials
#				and a list containing the label of each trial
# DESCRIPTION:	Applies a Butterworth filter and a smoothing filter over the data
#				in each file. Then calls to_trials() to standardize and split into trials
	"""

	lowcut 				= global_variables.get_lowcut()
	highcut 			= global_variables.get_highcut()
	fs 					= global_variables.get_sample_rate()
	order 				= global_variables.get_order()
	samples_per_trial 	= global_variables.get_samples_per_trial()
	files 				= global_variables.get_files_to_process()

	hor_tmp 	= []
	ver_tmp 	= []
	labels_tmp 	= []
	hor_file 	= []
	ver_file 	= []
	lab_file 	= []
	hor_bnd 	= []
	ver_bnd 	= []
	hor_sm 		= []
	ver_sm 		= []
# Arrays with horizontal and vertical components & labels of each sample
	hor = []
	ver = []
	lab = []

	print("\nStart filtering. \n\n      Cut Frequency: ", highcut, "\n      Order: ", order)

# Read file by file
	for file_name in files:
		hor_tmp, ver_tmp, labels_tmp = read.read_file(file_name)

		hor_file.extend(hor_tmp)
		ver_file.extend(ver_tmp)
		lab_file.extend(labels_tmp)

# Split all data into trials & standardize over trials
	trial_hor, trial_ver, trial_lab = tri.to_trials(hor_file, ver_file, lab_file)
	
# Data Padding with the sample	
	for iter in range(0, len(trial_hor)):
		new_hor = np.repeat(trial_hor[iter],3)
		new_ver = np.repeat(trial_ver[iter],3)
			
# Butterworth lowpass filter file by file

		sos = signal.butter(order, highcut, 'lowpass', analog=False, output='sos', fs=fs)
		hor_bnd = signal.sosfilt(sos, new_hor)
		ver_bnd = signal.sosfilt(sos, new_ver)

#Removing Data Padding
		hor_bnd = hor_bnd[len(trial_hor[iter]):len(hor_bnd)-len(trial_hor[iter])]
		ver_bnd = ver_bnd[len(trial_ver[iter]):len(ver_bnd)-len(trial_ver[iter])]
		
# Smoothing filter file by file
		hor_sm = signal.medfilt(hor_bnd, kernel_size = 35)
		ver_sm = signal.medfilt(ver_bnd, kernel_size = 35)
		
# Concatenate the results into ver and hor variables & labels
		hor.append(hor_sm)
		ver.append(ver_sm)

	lab = trial_lab
		
	return hor, ver, lab


def original_filter():
	"""
# FUNCTION:	 	filter()
# INPUT: 		None
# OUTPUT: 		Vertical & horizontal components of the data divided by trials
#				and a list containing the label of each trial
# DESCRIPTION:	Applies a Butterworth filter and a smoothing filter over the data
#				in each file. Then calls to_trials() to standardize and split into trials
#	"""

	lowcut 				= global_variables.get_lowcut()
	highcut 			= global_variables.get_highcut()
	fs 					= global_variables.get_sample_rate()
	order 				= global_variables.get_order()
	samples_per_trial 	= global_variables.get_samples_per_trial()
	files 				= global_variables.get_files_to_process()

	hor_tmp 	= []
	ver_tmp 	= []
	labels_tmp 	= []
	hor_bnd 	= []
	ver_bnd 	= []
	hor_sm 		= []
	ver_sm 		= []
# Arrays with horizontal and vertical components & labels of each sample
	hor = []
	ver = []
	lab = []

	print("\nStart filtering. \n\n      Cut Frequency: ", highcut, "\n      Order: ", order)

# Read file by file
	for file_name in files:
		hor_tmp, ver_tmp, labels_tmp = read.read_file(file_name)
		
# Butterworth lowpass filter file by file
		sos = signal.butter(order, highcut, 'lowpass', analog=False, output='sos', fs=fs)
		hor_bnd = signal.sosfilt(sos, hor_tmp)
		ver_bnd = signal.sosfilt(sos, ver_tmp)

# Smoothing filter file by file
		hor_sm = signal.medfilt(hor_bnd, kernel_size = 35)
		ver_sm = signal.medfilt(ver_bnd, kernel_size = 35)
# Concatenate results into ver and hor variables & labels
		hor.extend(hor_sm)
		ver.extend(ver_sm)
		lab.extend(labels_tmp)

# Split all data into trials & standardize over trials
	trial_hor, trial_ver, trial_lab = tri.to_trials(hor, ver, lab)
	return trial_hor, trial_ver, trial_lab


def online_filter(data):
	"""
# FUNCTION:	 	online_filter(data)
# INPUT: 		List with online data to be filtered
# OUTPUT: 		Vertical & horizontal components of the online data already filtered
# DESCRIPTION:	Applies a Butterworth filter and a smoothing filter over the data
#				in each file. Then calls to_trials() to standardize and split into trials
	"""

	lowcut 		= global_variables.get_lowcut()
	highcut 	= global_variables.get_highcut()
	fs 			= global_variables.get_sample_rate()
	order 		= global_variables.get_order()

# Standardize data
	data_mean 	= np.mean(data)
	data_sd 	= np.std(data)

	data_std = np.zeros(len(data))

	for s in range(0, len(data)):
		data_std[s] = (data[s] - data_mean) / data_sd

# Replicate signal
	rep_data = np.repeat(data_std,3)

# Apply Butterworth lowpass filter
	sos = signal.butter(order, highcut, 'lowpass', analog=False, output='sos', fs=fs)
	data_but = signal.sosfilt(sos, rep_data)

# Remove padding
	data_but = data_but[len(data):len(data_but)-len(data)]

# Apply Smoothing filter
	data_sm = signal.medfilt(data_but, kernel_size = 35)

	return data_sm