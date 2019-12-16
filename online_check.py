####################################################################
####################################################################

## PROBABLEMENTE FUNCION INUTIL

####################################################################
####################################################################

import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter
from datetime import datetime
import pickle
from sklearn.svm import SVC

import global_variables
import split_into_trials as tri
import plots
import read_function as read
import feature_extraction as feat


if __name__ == '__main__':

	files = ('/Users/jayromartinez/Dropbox/OpenBCI/data/Bloque_6.txt', '/Users/jayromartinez/Dropbox/OpenBCI/data/Bloque_7.txt',  '/Users/jayromartinez/Dropbox/OpenBCI/data/Bloque_8.txt', '/Users/jayromartinez/Dropbox/OpenBCI/data/Bloque_9.txt')
	labels = ['Up', 'Down', 'Left', 'Right']
	model_name = '/Users/jayromartinez/Dropbox/OpenBCI/models/bloque6_9_acc892_3Feat.sav'
	model = pickle.load(open(model_name, 'rb'))

	hor = []
	ver = []
	lab = []
	
	aciertos = 0
	pseudo_aciertos = 0
	predicted = []

	for file_name in files:
		hor_tmp = []
		ver_tmp = []
		lab_tmp = []
		hor_tmp, ver_tmp, lab_tmp = read.read_file(file_name)

		for i in range(0, len(hor_tmp)):
			if lab_tmp[i] != "'beep'":
				hor.append(float(hor_tmp[i]))
				ver.append(float(ver_tmp[i]))
				lab.append(lab_tmp[i])

	split_indx = range(750, len(hor), 750)
	trial_hor = np.split(hor, split_indx)
	trial_ver = np.split(ver, split_indx)
	trial_lab = np.split(lab, split_indx)

	for tr in range(0, len(trial_lab)):
		trial_lab[tr] = trial_lab[tr][0]

	for trial in range(0, len(trial_hor)):
		ver_mean = np.mean(trial_ver[trial])
		ver_sd = np.std(trial_ver[trial])
		hor_mean = np.mean(trial_hor[trial])
		hor_sd = np.std(trial_hor[trial])
		
		for t in (range(0, len(trial_ver[trial]))):
			trial_ver[trial][t] = (trial_ver[trial][t] - ver_mean) / ver_sd
			trial_hor[trial][t] = (trial_hor[trial][t] - hor_mean) / hor_sd

		sos = signal.butter(2, [0.03, 15], 'bandpass', analog=False, output='sos', fs=250)

		new_trial_hor = []
		new_trial_ver = []

		hor_zeros = np.random.normal(hor_mean,hor_sd,5000)

		ver_zeros = np.random.normal(ver_mean,ver_sd,5000)
		
		hor_end_add = np.append(trial_hor[trial],hor_zeros)
		hor_begg_add = np.append(hor_zeros, hor_end_add)
		ver_end_add = np.append(trial_ver[trial],ver_zeros)
		ver_begg_add = np.append(ver_zeros, ver_end_add)
		
		new_trial_hor = hor_begg_add
		new_trial_ver = ver_begg_add

		hor_bnd_aux = signal.sosfilt(sos, new_trial_hor)
		ver_bnd_aux = signal.sosfilt(sos, new_trial_ver)

		new_hor = hor_bnd_aux[5000:len(hor_bnd_aux)-5000]
		new_ver = ver_bnd_aux[5000:len(ver_bnd_aux)-5000]

		hor_sm = signal.medfilt(new_hor, kernel_size = 35)
		ver_sm = signal.medfilt(new_ver, kernel_size = 35)

		features = np.zeros(6)

		features[0] = np.min(hor_sm) # Horizontal Min 
		features[1] = np.min(ver_sm) # Vertical Min
		
		features[2] = np.max(hor_sm) # Horizontal Max
		features[3] = np.max(ver_sm) # Vertical Max
		
		features[4] = np.median(hor_sm) # Horizontal Median
		features[5] = np.median(ver_sm) # Vertical Median

		probs = model.predict_proba([features])

		labels.sort()
		max_pos = int(np.where(probs[0] == np.amax(probs[0]))[0])
		predicted = "'"+labels[max_pos]+"'"

		print("\nReal: ", trial_lab[trial], ", Predicted: ", predicted)

		if predicted == trial_lab[trial]:
			pseudo_aciertos += 1
			print("Pseudoacierto")
			if np.amax(probs) > 0.7:
				aciertos +=1
				print("Acierto")
		else:
			print("Ñau")

	print("\n\nNumero total de pseudoaciertos: ", pseudo_aciertos, "de ", len(trial_hor), ". ", round(pseudo_aciertos/len(trial_hor)*100,3),"%")
	print("Numero total de Aciertos: ", aciertos, "de ", len(trial_hor), ". ", round(aciertos/len(trial_hor)*100,3),"%")








	
