####################################################################
####################################################################

## PROBABLEMENTE FUNCION INUTIL

####################################################################
####################################################################
from openbci import cyton as board
import time
from pydub import AudioSegment
from pydub.playback import play
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter
from scipy import stats
from matplotlib.collections import LineCollection
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier


##############################################################################
##############################################################################
def trial_plot(trial_hor, trial_ver, trial_lab):

	hor = []
	ver = []
	
	for i in range(0, len(trial_lab)):
		for j in range(0, len(trial_hor[i])):
				hor.append(trial_hor[i][j])
				ver.append(trial_ver[i][j])
	
	plt.subplot(211)
	plt.plot(range(0, len(ver)), ver)
	plt.title(" Ver")
	plt.xticks(np.arange(0,len(ver), step=750))
	#plt.yticks(np.arange(min(ver), max(ver), step=step_ver))
	#plt.yticks(np.arange(min(ver), max(ver)))
	for j in range(0,len(ver), 750):
		plt.axvline(x=j, color='tab:gray', linestyle=':')
	#plt.axvline(x=j, color='tab:gray', linestyle=':')
	#plt.show()

	#step_hor = max(hor) - min(hor) / 10
	plt.subplot(212)
	plt.plot(range(0, len(hor)), hor)
	plt.title(" Hor")
	plt.xticks(np.arange(0,len(hor), step=750))
	#plt.yticks(np.arange(min(hor), max(hor), step=step_hor))
	#plt.yticks(np.arange(min(hor), max(hor)))
	for j in range(0,len(hor), 750):
		plt.axvline(x=j, color='tab:gray', linestyle=':')
	plt.show()




##############################################################################
##############################################################################
def movement_plot(trial_hor, trial_ver, trial_lab, movement):

	hor = []
	ver = []

	for i in range(0, len(trial_lab)):
		if trial_lab[i] == movement:
			for j in range(0, len(trial_hor[i])):
				hor.append(trial_hor[i][j])
				ver.append(trial_ver[i][j])



	#step_ver = max(ver) - min(ver) / 10
	plt.subplot(211)
	plt.plot(range(0, len(ver)), ver)
	plt.title(movement+" Ver")
	plt.xticks(np.arange(0,len(ver), step=750))
	#plt.yticks(np.arange(min(ver), max(ver), step=step_ver))
	#plt.yticks(np.arange(min(ver), max(ver)))
	for j in range(0,len(ver), 750):
		plt.axvline(x=j, color='tab:gray', linestyle=':')
	#plt.axvline(x=j, color='tab:gray', linestyle=':')
	#plt.show()

	#step_hor = max(hor) - min(hor) / 10
	plt.subplot(212)
	plt.plot(range(0, len(hor)), hor)
	plt.title(movement+" Hor")
	plt.xticks(np.arange(0,len(hor), step=750))
	#plt.yticks(np.arange(min(hor), max(hor), step=step_hor))
	#plt.yticks(np.arange(min(hor), max(hor)))
	for j in range(0,len(hor), 750):
		plt.axvline(x=j, color='tab:gray', linestyle=':')
	plt.show()


##############################################################################
##############################################################################
def feature_plot(feat, to_plot):
	
	feature_list = ["Min","Max","Median","Mode","Kurtosis","Max_position","Min_position","AUC","First_q","Third_q","Interquartile", "Derivative Slope"]
	feature_index = feature_list.index(to_plot)

	up_ver_feat = []
	down_ver_feat = []
	left_ver_feat = []
	right_ver_feat = []

	up_hor_feat = []
	down_hor_feat = []
	left_hor_feat = []
	right_hor_feat = []

	for iter in range(0, len(trial_lab)):
		if trial_lab[iter] == "'Up'":
			up_hor_feat.append(feat[iter][2*feature_index])
			up_ver_feat.append(feat[iter][2*feature_index+1])
		elif trial_lab[iter] == "'Down'":
			down_hor_feat.append(feat[iter][2*feature_index])
			down_ver_feat.append(feat[iter][2*feature_index+1])
		elif trial_lab[iter] == "'Left'":
			left_hor_feat.append(feat[iter][2*feature_index])
			left_ver_feat.append(feat[iter][2*feature_index+1])
		elif trial_lab[iter] == "'Right'":
			right_hor_feat.append(feat[iter][2*feature_index])
			right_ver_feat.append(feat[iter][2*feature_index+1])

	data = [up_hor_feat,down_hor_feat,left_hor_feat,right_hor_feat,up_ver_feat,down_ver_feat,left_ver_feat,right_ver_feat]

	fig, ax = plt.subplots()

	plot_labels = ["Up Hor", "Up Ver", "Down Hor","Down Ver", "'Left Hor'","'Left Ver'", "'Right Hor'","'Right Ver'"]
	ax.set_xticklabels(plot_labels)
	ax.set_title(to_plot)
	plt.yticks(np.arange(-1,1))

	ax.boxplot(data)
	plt.show()


##############################################################################
##############################################################################
def classification(feat, trial_lab):
# Split Features and Labels into train & test
	test_size = 0.33
	feat_train, feat_test, trial_lab_train, trial_lab_test = train_test_split(feat, 
																			  trial_lab,
																			  test_size = test_size)
# Train model and predict labels
	clf = SVC(C=1.75, kernel='linear', gamma='scale', decision_function_shape='ovo')
	
	scores = cross_val_score(clf, feat, trial_lab, cv=10)
	print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

	#clf.fit(feat_train, trial_lab_train)
	#print("Accuracy: ", clf.score(feat_test, trial_lab_test))

	#clf = MLPClassifier(activation='tanh', solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(75, 65, 55, 45, 35, 25, 15, 10), max_iter=10000, random_state=1)
	#clf.fit(feat_train, trial_lab_train)
	#print("Accuracy: ", clf.score(feat_test, trial_lab_test))

##############################################################################
##############################################################################
def features(trial_hor, trial_ver):

	num_feat = 24 # Number of Features (12 vertical and 12 horizontal)
	features = np.zeros((len(trial_hor), num_feat))

	#tmp_der_hor = []
	#tmp_der_ver = []

	for iter in range(0, len(trial_hor)):
		
		features[iter][0] = np.min(trial_hor[iter]) # Horizontal Min 
		features[iter][1] = np.min(trial_ver[iter]) # Vertical Min
		
		features[iter][2] = np.max(trial_hor[iter]) # Horizontal Max
		features[iter][3] = np.max(trial_ver[iter]) # Vertical Max
		
		features[iter][4] = np.median(trial_hor[iter]) # Horizontal Median
		features[iter][5] = np.median(trial_ver[iter]) # Vertical Median

		features[iter][6] = float(stats.mode(trial_hor[iter])[0]) # Horizontal Mode
		features[iter][7] = float(stats.mode(trial_ver[iter])[0]) # Vertical Mode

		features[iter][8] = stats.kurtosis(trial_hor[iter], nan_policy='omit') # Horizontal Kurtosis
		features[iter][9] = stats.kurtosis(trial_ver[iter], nan_policy='omit') # Vertical Kurtosis

		features[iter][10] = int(np.where(trial_hor[iter] == np.max(trial_hor[iter]))[0][0]) # Horizontal Max position
		features[iter][11] = int(np.where(trial_ver[iter] == np.max(trial_ver[iter]))[0][0]) # Vertical Max position

		features[iter][12] = int(np.where(trial_hor[iter] == np.min(trial_hor[iter]))[0][0]) # Horizontal Min position
		features[iter][13] = int(np.where(trial_ver[iter] == np.min(trial_ver[iter]))[0][0]) # Vertical Min position
		
		features[iter][17] = sum(abs(trial_hor[iter])) # Horizontal Area under the curve
		features[iter][15] = sum(abs(trial_ver[iter])) # Vertical Area under the curve

		features[iter][16] = np.percentile(trial_hor[iter], 25) # Horizontal First quartile
		features[iter][17] = np.percentile(trial_ver[iter], 25) # Vertical First quartile

		features[iter][18] = np.percentile(trial_hor[iter], 75) # Horizontal Third quartile
		features[iter][19] = np.percentile(trial_ver[iter], 75) # Vertical Third quartile

		features[iter][20] = np.percentile(trial_hor[iter], 75) - np.percentile(trial_hor[iter], 25) # Horizontal Interquartile range
		features[iter][21] = np.percentile(trial_ver[iter], 75) - np.percentile(trial_ver[iter], 25) # Vertical Interquartile range
		

# Calculate derivative & derivative slope
		der_hor = np.zeros(len(trial_hor[iter]))
		der_ver = np.zeros(len(trial_ver[iter]))

		pos_min_der_hor = []
		pos_max_der_hor = []
		pos_min_der_ver = []
		pos_max_der_ver = []

		min_der_hor = 0
		max_der_hor = 0
		min_der_ver = 0
		max_der_ver = 0

		for j in range(5, len(trial_hor[iter])):
			der_hor[j] = (trial_hor[iter][j] - trial_hor[iter][j-5]) / 5
			der_ver[j] = (trial_ver[iter][j] - trial_ver[iter][j-5]) / 5
		
		#tmp_der_hor.append(der_hor)
		#tmp_der_ver.append(der_ver)

		min_der_hor = np.min(der_hor)
		max_der_hor = np.max(der_hor)
		min_der_ver = np.min(der_ver)
		max_der_ver = np.max(der_ver)

		pos_min_der_hor = int(np.where(der_hor == min_der_hor)[0][0])
		pos_max_der_hor = int(np.where(der_hor == max_der_hor)[0][0])
		pos_min_der_ver = int(np.where(der_ver == min_der_ver)[0][0])
		pos_max_der_ver = int(np.where(der_ver == max_der_ver)[0][0])

		features[iter][22] = abs(max_der_hor - min_der_hor) / (pos_max_der_hor - pos_min_der_hor)# Horizontal Derivative Slope
		features[iter][23] = abs(max_der_ver - min_der_ver) / (pos_max_der_ver - pos_min_der_ver)# Vertical Derivative Slope


	#movement="'Down'"
	#movement_plot(tmp_der_hor, tmp_der_ver, trial_lab, movement)

	return features


##############################################################################
##############################################################################
def to_trials(hor, ver, lab):
# Split intro trials
	split_indx = range(750, len(lab), 750)
	trial_hor = np.split(hor, split_indx)
	trial_ver = np.split(ver, split_indx)
	trial_lab = np.split(lab, split_indx)

# Remove 'beep' trials
	tri = 0
	while tri<len(trial_lab):
		if (trial_lab[tri][0] == "'beep'") or (trial_lab[tri][0] == "'Blink'") or (trial_lab[tri][0] == "'Double_Blink'") or (trial_lab[tri][0] == "'Close_Eyes'"):
			del trial_lab[tri]
			del trial_ver[tri]
			del trial_hor[tri]
		else:
			tri += 1

# Standarize over samples
	for s in (range(0, len(trial_lab))):
		#Reduce the labels to only one
		trial_lab[s] = trial_lab[s][0]
		# STANDARIZATION OVER SAMPLES
		ver_mean = np.mean(trial_ver[s])
		ver_sd = np.std(trial_ver[s])
		hor_mean = np.mean(trial_hor[s])
		hor_sd = np.std(trial_hor[s])
		ver_max = np.max(trial_ver[s])
		hor_max = np.max(trial_hor[s])

		for t in (range(0, len(trial_ver[s]))):
			trial_ver[s][t] = (trial_ver[s][t] - ver_mean) / ver_sd
			trial_hor[s][t] = (trial_hor[s][t] - hor_mean) / hor_sd
			#print(trial_hor[s][t])

	return trial_hor, trial_ver, trial_lab


##############################################################################
##############################################################################
def read_file(file_name):
# Open the file
	file = open(file_name, 'r')
	values = file.readlines()
	
# Load data into new_values
	new_values = []
	labels_tmp = []
	hor_tmp = []
	ver_tmp = []

	for v in range(0,len(values)):
		new_values.insert(v, values[v].split(','))

# Load data from new_values into labels, horizontal & vertical
	for i in range(0,len(new_values)):
		labels_tmp.append(new_values[i][0])
		hor_tmp.append(new_values[i][2])
		ver_tmp.append(new_values[i][7])

# Remove '[' and cast into float
	for aux in range(0, len(labels_tmp)):
		if labels_tmp[aux].find("[") != -1:
			index = labels_tmp[aux].find("[")
			labels_tmp[aux] = labels_tmp[aux].replace(labels_tmp[aux][index], '')
			hor_tmp[aux] =float(hor_tmp[aux])
			ver_tmp[aux] =float(ver_tmp[aux])
		else:
			hor_tmp[aux] =float(hor_tmp[aux])
			ver_tmp[aux] =float(ver_tmp[aux])

	return hor_tmp, ver_tmp, labels_tmp


##############################################################################
##############################################################################
def filter(files):
	lowcut = 0.01
	highcut = 35
	fs = 250
	order = 4

	hor_tmp = []
	ver_tmp = []
	labels_tmp = []
	hor_bnd = []
	ver_bnd = []
	hor_sm = []
	ver_sm = []
# Arrays with horizontal and vertical components & labels of each sample
	hor = []
	ver = []
	lab = []


# Read file by file
	for file_name in files:
		hor_tmp, ver_tmp, labels_tmp = read_file(file_name)

# Butterworth bandpas filter file by file
#		sos = signal.butter(order, [lowcut, highcut], 'bandpass', analog=False, output='sos', fs=250)
#		hor_bnd = signal.sosfilt(sos, hor_tmp)
#		ver_bnd = signal.sosfilt(sos, ver_tmp)

# Butterworth bandpas filter file by file
		[b,a] = signal.butter(order, [lowcut, highcut], 'bandpass', analog=False, output='ba', fs=250)
		hor_bnd = signal.filtfilt(b,a, hor_tmp)
		ver_bnd = signal.filtfilt(b,a, ver_tmp)

# IIR Filter
#		[b,a] = signal.iirfilter(order, [lowcut, highcut],btype='bandpass',analog=True, output='ba')
#		hor_bnd = signal.filtfilt(b, a, hor_tmp)
#		ver_bnd = signal.filtfilt(b, a, ver_tmp)
#		print(hor_bnd)

# Smoothing filter file by file
		hor_sm = signal.medfilt(hor_bnd, kernel_size = 35)
		ver_sm = signal.medfilt(ver_bnd, kernel_size = 35)
# Concatenate the results into ver and hor variables & labels
		hor.extend(hor_sm)
		ver.extend(ver_sm)
		lab.extend(labels_tmp)

# Split all data into trials & standarize over trials
	trial_hor, trial_ver, trial_lab = to_trials(hor, ver, lab)

	return trial_hor, trial_ver, trial_lab


##############################################################################
##############################################################################
def handle_streamed_data(sample):
	
	tmp_lab = labels[iter]

	if cont == 0:
		if tmp_lab == 'EXIT':
			file.close()
			wh.connection.stop()
			wh.connection.disconnect()
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


##############################################################################
##############################################################################
def acquire_save():
	connection.print_register_settings()  
	connection.start_streaming(handle_streamed_data)
	connection.loop()


##############################################################################
##############################################################################
def data(filename):
# Create labels, random shuffle & insert 5 beeps at the beginning
	lab = ['Up', 'Down', 'Left', 'Right', 'Blink', 'Double_Blink', 'Close_Eyes']
	labels = lab*10
	random.shuffle(labels)
	for i in range(0,5):
		labels.insert(0,"beep")
	labels.append('EXIT')
# open file were we are going to save the data
	file = open(filename, 'w')
# Create an iterator over label array
	iter = 0
# Create a counter for the number of datapoints (250 per second, 750 per trial)
	cont = 0
# Call to aquire_save function
	acquire_save()


##############################################################################
##############################################################################
def connect():

# CONNECTION PARAMETERS
	port = '/dev/tty.usbserial-DM01HL5T'
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
	connection.ser.write(b'x2040000X')
	connection.ser.write(b'x7040000X')

	return connection


##############################################################################
##############################################################################
def connect_acquire_store(filename):

# Connection & Configuration
	connection = connect()

# Data Acquisition & Data Storage
	data(filename)


##############################################################################
##############################################################################
if __name__ == '__main__':

# Connection, Data Acquisition & Data Storage
	# Name of the file where to save the data
	filename = "Bloque_6.txt"
	connect_acquire_store(filename)

# Data Load, Filtering & Trial Split
	# Files that we want to load & filter
#	files = ["Bloque_1.txt", "Bloque_2.txt", "Bloque_3.txt", "Bloque_4.txt", "Bloque_5.txt"]
#	trial_hor, trial_ver, trial_lab = filter(files)

	#movement="'Down'"
	#movement_plot(trial_hor, trial_ver, trial_lab, movement)

	#trial_plot(trial_hor, trial_ver, trial_lab)

# Feature Extraction
#	feat = features(trial_hor, trial_ver)

# Features Plot
	#to_plot = 'Derivative Slope'
	#feature_plot(feat, to_plot=to_plot)
# Classification
#	classification(feat, trial_lab)


