####################################################################
####################################################################

## PROBABLEMENTE FUNCION INUTIL

####################################################################
####################################################################
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter
from scipy import stats
from matplotlib.collections import LineCollection


if __name__ == '__main__':

################################################
# OPEN FILE AND GET THE DATA                   #
################################################
	
	file = open("Jayro_5.txt", 'r')
	values = file.readlines()
	#print values
	new_values = []
	for v in range(0,len(values)):
		new_values.insert(v, values[v].split(','))

################################################
# BANDPASS, SMOOTHING AND NORMALIZATION        #
################################################
	
	x = range(1,len(new_values))
	
	#labels = []
	hor = []
	ver = []
	hor_filt = []
	ver_filt = []
	labels = []
	ver_norm = []
	hor_norm = []
	
	for i in range(1,len(new_values)):
		labels.append(new_values[i][0])
		hor.append(new_values[i][2])
		ver.append(new_values[i][7])

	for aux in range(0, len(labels)):
		if labels[aux].find("[") != -1:
			index = labels[aux].find("[")
			labels[aux] = labels[aux].replace(labels[aux][index], '')
			hor[aux] =float(hor[aux])
			ver[aux] =float(ver[aux])
		else:
			hor[aux] =float(hor[aux])
			ver[aux] =float(ver[aux])

	lowcut = 0.01
	highcut = 35
	fs = 250
	order = 10
# Bandpass Filter
	sos = signal.butter(order, [lowcut, highcut], 'bandpass', analog=False, output='sos', fs=250)
	hor_filt = signal.sosfilt(sos, hor)
	ver_filt = signal.sosfilt(sos, ver)

# Normalization using whole dataset (We don't use it, we normalize over samples)
#	ver_mean = np.mean(ver_filt)
#	ver_sd = max(abs(ver_filt))
#	hor_mean = np.mean(hor_filt)
#	hor_sd = max(abs(hor_filt))
#
#
#	ver_norm = []
#	hor_norm = []
#	for iter in range(0, len(ver)-1):
#		ver_norm.append((ver_filt[iter] - ver_mean) / ver_max)
#		hor_norm.append((hor_filt[iter] - hor_mean) / hor_max)
# Smoothing Filter
	hor_def = signal.medfilt(hor_filt, kernel_size = 35)
	ver_def = signal.medfilt(ver_filt, kernel_size = 35)

#	hor_def = hor
#	ver_def = ver

###########################################
# 	SPLIT DATA BY ACTIONS			      #
###########################################
#	colors = []
#	up_hor = []
#	up_ver = []
#	down_hor = []
#	down_ver = []
#	left_hor = []
#	left_ver = []
#	right_hor = []
#	right_ver = []
#	blink_hor = []
#	blink_ver = []
#	double_blink_hor = []
#	double_blink_ver = []
#	close_eyes_hor = []
#	close_eyes_ver = []
#
#	for i in range(0,len(labels)):
#		if labels[i] == "'Up'":
#			colors.append('k')
#			up_hor.append(hor_def[i])
#			up_ver.append(ver_def[i])
#		elif labels[i] == "'Down'":
#			colors.append('tab:green')
#			down_hor.append(hor_def[i])
#			down_ver.append(ver_def[i])
#		elif labels[i] == "'Left'":
#			colors.append('tab:orange')
#			left_hor.append(hor_def[i])
#			left_ver.append(ver_def[i])
#		elif labels[i] == "'Right'":
#			colors.append('tab:red')
#			right_hor.append(hor_def[i])
#			right_ver.append(ver_def[i])
#		elif labels[i] == "'Blink'":
#			colors.append('tab:blue')
#			blink_hor.append(hor_def[i])
#			blink_ver.append(ver_def[i])
#		elif labels[i] == "'Double_Blink'":
#			colors.append('tab:pink')
#			double_blink_hor.append(hor_def[i])
#			double_blink_ver.append(ver_def[i])
#		elif labels[i] == "'Close_Eyes'":
#			colors.append('tab:brown')
#			close_eyes_hor.append(hor_def[i])
#			close_eyes_ver.append(ver_def[i])
#		else:
#			colors.append('tab:gray')
	
###########################################
# 	PLOT COMPARISON BETWEEN TWO SIGNALS   #
###########################################
#	lines_ver = [((x0,ver0), (x1,ver1)) for x0, ver0, x1, ver1 in zip(x[:-1], ver[:-1], x[1:], ver[1:])]
#	lines_hor = [((x0,hor0), (x1,hor1)) for x0, hor0, x1, hor1 in zip(x[:-1], hor[:-1], x[1:], hor[1:])]
#	#colored_lines = LineCollection(lines, colors=colors, linewidths=(2,))
#	colored_lines_ver = LineCollection(lines_ver, colors=colors, linewidths=(2,), linestyle = '-', label='Vertical')
#	colored_lines_hor = LineCollection(lines_hor, colors=colors, linewidths=(1,), linestyle = ':', label='Horizontal')
#
#	lines_ver_filt = [((x0,def_ver0), (x1,def_ver1)) for x0, def_ver0, x1, def_ver1 in zip(x[:-1], def_ver[:-1], x[1:], def_ver[1:])]
#	lines_hor_filt = [((x0,def_hor0), (x1,def_hor1)) for x0, def_hor0, x1, def_hor1 in zip(x[:-1], def_hor[:-1], x[1:], def_hor[1:])]
#	#colored_lines = LineCollection(lines, colors=colors, linewidths=(2,))
#	colored_lines_ver_norm = LineCollection(lines_ver_filt, colors=colors, linewidths=(2,), linestyle = '-', label='Vertical_NORM')
#	colored_lines_hor_norm = LineCollection(lines_hor_filt, colors=colors, linewidths=(1,), linestyle = ':', label='Horizontal_NORM')
#	lines_ver_filt2 = [((x0,ver_filt20), (x1,ver_filt21)) for x0, ver_filt20, x1, ver_filt21 in zip(x[:-1], ver_filt2[:-1]-2000, x[1:], ver_filt2[1:]-2000)]
#	lines_hor_filt2 = [((x0,hor_filt20), (x1,hor_filt21)) for x0, hor_filt20, x1, hor_filt21 in zip(x[:-1], hor_filt2[:-1], x[1:], hor_filt2[1:])]
#	#colored_lines = LineCollection(lines, colors=colors, linewidths=(2,))
#	colored_lines_ver_filt2 = LineCollection(lines_ver_filt2, colors=colors, linewidths=(2,), linestyle = '-', label='Vertical_filt')
#	colored_lines_hor_filt2 = LineCollection(lines_hor_filt2, colors=colors, linewidths=(1,), linestyle = ':', label='Horizontal_filt')
#
#
#	fig, ax = plt.subplots(2,1)
#	ax[0].add_collection(colored_lines_ver_norm)
#	ax[0].add_collection(colored_lines_hor_norm)
#	ax[0].autoscale_view()
#	ax[0].legend()
#	for j in range(0,len(x)-1, 750):
#		ax[0].axvline(x=j, color='tab:gray', linestyle=':')
#	
#	ax[1].add_collection(colored_lines_ver_filt2)
#	ax[1].add_collection(colored_lines_hor_filt2)
#	ax[1].autoscale_view()
#	ax[1].legend()
#	for j in range(0,len(x)-1, 750):
#		ax[1].axvline(x=j, color='tab:gray', linestyle=':')
#	
#	plt.show()

########################################################################
# PLOTS FOR VERTICAL & HORIZONTAL COMPONENTS OF SAME TYPE OF MOVEMENT  #
########################################################################
#	
#	step_ver = max(right_ver) - min(right_ver) / 10
#	plt.subplot(211)
#	plt.plot(range(0, len(right_ver)), right_ver)
#	plt.title("right_ver")
#	plt.xticks(np.arange(0,len(right_ver),step=750))
#	plt.yticks(np.arange(min(right_ver), max(right_ver), step=step_ver))
#	for j in range(0,len(right_ver), 750):
#		plt.axvline(x=j, color='tab:gray', linestyle=':')
#	#plt.axvline(x=j, color='tab:gray', linestyle=':')
#	#plt.show()
#
#	step_hor = max(right_hor) - min(right_hor) / 10
#	plt.subplot(212)
#	plt.plot(range(0, len(right_hor)), right_hor)
#	plt.title("right_hor")
#	plt.xticks(np.arange(0,len(right_hor),step=750))
#	plt.yticks(np.arange(min(right_hor), max(right_hor), step=step_hor))
#	for j in range(0,len(right_hor), 750):
#		plt.axvline(x=j, color='tab:gray', linestyle=':')
#	plt.show()

################################################
# SPLIT THE DATA INTO SAMPLES                  #
################################################
	
	samples_hor = []
	samples_ver = []
	samples_label = []

	samples_hor_min = []
	samples_hor_max = []
	#samples_hor_mean = []
	samples_hor_median = []
	samples_hor_mode = []
	#samples_hor_sd = []
	samples_hor_kurtosis = []
	samples_hor_max_position = []
	samples_hor_min_position = []
	samples_hor_area_under_curve = []
	#samples_hor_entropy = []
	samples_hor_first_quartile = []
	samples_hor_third_quartile = []
	samples_hor_interquartile_range = []

	samples_ver_min = []
	samples_ver_max = []
	#samples_ver_mean = []
	samples_ver_median = []
	samples_ver_mode = []
	#samples_ver_sd = []
	samples_ver_kurtosis = []
	samples_ver_max_position = []
	samples_ver_min_position = []
	samples_ver_area_under_curve = []
	#samples_ver_entropy = []
	samples_ver_first_quartile = []
	samples_ver_third_quartile = []
	samples_ver_interquartile_range = []
	# Should we include slope of max--min segment in first derivative¿?

	split_indx = range(749, len(labels), 750)
	samples_hor = np.split(hor_def, split_indx)
	samples_ver = np.split(ver_def, split_indx)
	samples_label = np.split(labels, split_indx)

	for s in (range(0, len(samples_hor))):
		#Reduce the labels to only one
		samples_label[s] = samples_label[s][0]
		# NORMALIZATION OVER SAMPLES
		ver_mean = np.mean(samples_ver[s])
		ver_sd = np.std(samples_ver[s])
		hor_mean = np.mean(samples_hor[s])
		hor_sd = np.std(samples_hor[s])

		for t in (range(0, len(samples_ver[s]))):
			samples_ver[s][t] = (samples_ver[s][t] - ver_mean) / ver_sd
			samples_hor[s][t] = (samples_hor[s][t] - hor_mean) / hor_sd

################################################
# FEATURE EXTRACTION FOR EACH SAMPLE           #
################################################

		samples_hor_min.append(min(samples_hor[s]))
		samples_hor_max.append(max(samples_hor[s]))
		# After Normalization Mean has no sense
		#samples_hor_mean.append(np.mean(samples_hor[s]))
		samples_hor_median.append(np.median(samples_hor[s]))
		samples_hor_mode.append(float(stats.mode(samples_hor[s])[0]))
		# After Normalization Standard Deviation has no sense
		#samples_hor_sd.append(np.std(samples_hor[s]))
		samples_hor_kurtosis.append(stats.kurtosis(samples_hor[s], nan_policy='omit'))
		samples_hor_max_position.append(int(np.where(samples_hor[s] == max(samples_hor[s]))[0][0]))
		samples_hor_min_position.append(int(np.where(samples_hor[s] == min(samples_hor[s]))[0][0]))
		samples_hor_area_under_curve.append(sum(abs(samples_hor[s])))
		#samples_hor_entropy.append(stats.entropy(samples_hor[s]))
		samples_hor_first_quartile.append(np.percentile(samples_hor[s], 25))
		samples_hor_third_quartile.append(np.percentile(samples_hor[s], 75))
		samples_hor_interquartile_range.append(np.percentile(samples_hor[s], 75) - np.percentile(samples_hor[s], 25))

		samples_ver_min.append(min(samples_ver[s]))
		samples_ver_max.append(max(samples_ver[s]))
		# After Normalization Mean has no sense
		#samples_ver_mean.append(np.mean(samples_ver[s]))
		samples_ver_median.append(np.median(samples_ver[s]))
		samples_ver_mode.append(float(stats.mode(samples_ver[s])[0]))
		# After Normalization Standard Deviation has no sense
		#samples_ver_sd.append(np.std(samples_ver[s]))
		samples_ver_kurtosis.append(stats.kurtosis(samples_ver[s], nan_policy='omit'))
		samples_ver_max_position.append(int(np.where(samples_ver[s] == max(samples_ver[s]))[0][0]))
		samples_ver_min_position.append(int(np.where(samples_ver[s] == min(samples_ver[s]))[0][0]))
		samples_ver_area_under_curve.append(sum(abs(samples_ver[s])))
		#samples_ver_entropy.append(stats.entropy(samples_ver[s]))
		samples_ver_first_quartile.append(np.percentile(samples_ver[s], 25))
		samples_hor_third_quartile.append(np.percentile(samples_ver[s], 75))
		samples_ver_interquartile_range.append(np.percentile(samples_ver[s], 75) - np.percentile(samples_ver[s], 25))

	
		