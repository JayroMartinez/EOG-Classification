import pickle
import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter

import read_function
import global_variables
import feature_extraction as feat
import plots

if __name__ == '__main__':

# MOSTRAMOS VENTANA PARA SELECCIONAR MODELO
	model_name = '/Users/jayromartinez/Documents/GitHub/EOG-Classification/models/patient4.sav'
# CARGAMOS EL MODELO
	model = pickle.load(open(model_name, 'rb'))

# MOSTRAMOS VENTANA PARA SELECCIONAR ARCHIVO ONLINE
	file_name = '/Users/jayromartinez/Documents/GitHub/EOG-Classification/data/patient9_online_data_4.txt'
# LEEMOS EL ARCHIVO
	trial_hor, trial_ver = read_function.read_online_file(file_name)
# MOSTRAMOS VENTANA PARA SELECCIONAR ARCHIVO AUXILIAR
	aux_file_name = '/Users/jayromartinez/Documents/GitHub/EOG-Classification/data/patient4_simulated_online_aux_data_1.txt'
# ABRIMOS Y LEEMOS EL ARCHIVO
	file = open(aux_file_name, 'r')
	values = file.readlines()
# GUARDAMOS EN TO_DO LAS ACCIONES QUE EL USUARIO HA REALIZADO
	new_values = []
	to_do = []
	for v in range(0,len(values)):
		new_values.insert(v, values[v].split(']'))
	for i in range(0, len(new_values)):
		if str(new_values[i]).find("TO DO") != -1 and str(new_values[i]).find("Up") != -1:
			to_do.append('Up')
		elif str(new_values[i]).find("TO DO") != -1 and str(new_values[i]).find("Down") != -1:
			to_do.append('Down')
		elif str(new_values[i]).find("TO DO") != -1 and str(new_values[i]).find("Left") != -1:
			to_do.append('Left')
		elif str(new_values[i]).find("TO DO") != -1 and str(new_values[i]).find("Right") != -1:
			to_do.append('Right')
	
# REALIZAMOS LOS CALCULOS Y LAS PREDICCIONES
	hor = []
	ver = []
	order = global_variables.get_order()
	highcut = global_variables.get_highcut()
	fs = global_variables.get_sample_rate()
	samples_per_trial = global_variables.get_samples_per_trial()
	
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
	# Plot Online Filtered Data
	plots.trial_plot(hor, ver, [])
	# Feature Extraction
	features = []
	features = feat.features(hor, ver)

	# Predict
	predicted = []
	lab = global_variables.get_lab()
	lab.sort()
	probs = model.predict_proba(features)
	for j in range(0, len(features)):
		if np.max(probs[j]) > 0.5:
			max_pos = int(np.where(probs[j] == np.max(probs[j]))[0])
			movement = lab[max_pos]
		else:
			movement = "Unknown"
		predicted.append(movement)

	aciertos = 0
	for k in range(0, len(to_do)):
		if to_do[k] == predicted[k]:
			aciertos +=1
	print("Total hit number ",aciertos, " out of ", len(to_do))
	print("Accuracy: ", round(aciertos/len(to_do)*100,2), "%")


