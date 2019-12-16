import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter
from datetime import datetime

import global_variables
import split_into_trials as tri
import plots
import read_function
import feature_extraction as feat
import svm_classification as classif

def pipeline():

	# Open the file
	file_name = global_variables.get_files_to_process()
	
	trial_hor, trial_ver = read_function.read_online_file(file_name[0])

	order = global_variables.get_order()
	lowcut = global_variables.get_lowcut()
	highcut = global_variables.get_highcut()
	fs = global_variables.get_sample_rate()

	hor = []
	ver = []

	for s in (range(0, len(trial_hor))):
		# STANDARIZATION OVER SAMPLES
		ver_mean = np.mean(trial_ver[s])
		ver_sd = np.std(trial_ver[s])
		hor_mean = np.mean(trial_hor[s])
		hor_sd = np.std(trial_hor[s])
		
		for t in (range(0, len(trial_ver[s]))):
			trial_ver[s][t] = (trial_ver[s][t] - ver_mean) / ver_sd
			trial_hor[s][t] = (trial_hor[s][t] - hor_mean) / hor_sd
		
	for iter in range(0, len(trial_hor)):
		new_hor = np.repeat(trial_hor[iter],3)
		new_ver = np.repeat(trial_ver[iter],3)
			
# Butterworth bandpas filter file by file

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
	
	# Feature Extraction
	features = []
	features = feat.features(hor, ver)

	# Classification
	#classif.classification(features, trial_lab)
	plots.trial_plot(hor, ver, [])
	


