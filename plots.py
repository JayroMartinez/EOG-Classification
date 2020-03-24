import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D

import global_variables

###################################################
# THIS FUNCTIONS ARE NOT INCLUDED IN THE PIPELINE #
###################################################
#   They are created as auxiliar functions that   #
#   could be called just in case they are needed  #
###################################################

def trial_plot(trial_hor, trial_ver, trial_lab):
	"""
# FUNCTION:	 	trial_plot(trial_hor, trial_ver)
# INPUT: 		Horizontal & Vertical components of each trial
# OUTPUT: 		Lineplot
# DESCRIPTION:	Generate the plots for horizontal and vertical values and
#				shows the division over samples
# TODO:			Add labels or colors based on labels
	"""

	hor = []
	ver = []

	samples_per_trial = global_variables.get_samples_per_trial()
	
	for i in range(0, len(trial_hor)):
		for j in range(0, len(trial_hor[i])):
				hor.append(trial_hor[i][j]/8)
				ver.append(trial_ver[i][j]/8)
	
	plt.subplot(211)
	plt.plot(range(0, len(ver)), ver)
	plt.title(" Ver")
	plt.xticks(np.arange(250,len(ver)+250, step=samples_per_trial),trial_lab, rotation=45, fontsize = 8)
	plt.ylabel('mV')
	
	for j in range(0,len(ver), samples_per_trial):
		plt.axvline(x=j, color='tab:gray', linestyle=':')
	
	plt.subplot(212)
	plt.plot(range(0, len(hor)), hor)
	plt.title(" Hor")
	plt.xticks(np.arange(250,len(hor)+250, step=samples_per_trial),trial_lab, rotation=45, fontsize = 8)
	plt.ylabel('mV')
	
	for j in range(0,len(hor), samples_per_trial):
		plt.axvline(x=j, color='tab:gray', linestyle=':')
	plt.show()


def derivative_signal(trial_hor, trial_ver, trial_lab):

	der_hor = []
	der_ver = []

	samples_per_trial = global_variables.get_samples_per_trial()
	
	for i in range(0, len(trial_hor)):
		hor = []
		ver = []
		for j in range(0, len(trial_hor[i])):
				hor.append(trial_hor[i][j])
				ver.append(trial_ver[i][j])
		der_hor.extend(np.gradient(hor, 5))
		der_ver.extend(np.gradient(ver,5))

	plt.subplot(211)
	plt.plot(range(0, len(der_ver)),der_ver)
	plt.title("Ver")
	plt.xticks(np.arange(samples_per_trial/2,len(der_ver)+samples_per_trial/2, step=samples_per_trial),trial_lab, rotation=45, fontsize = 8)
	
	for j in range(0,len(der_ver), samples_per_trial):
		plt.axvline(x=j, color='tab:gray', linestyle=':')
	
	plt.subplot(212)
	plt.plot(range(0, len(der_hor)),der_hor)
	plt.title("Hor")
	plt.xticks(np.arange(samples_per_trial/2,len(der_hor)+samples_per_trial/2, step=samples_per_trial),trial_lab, rotation=45, fontsize = 8)
	
	for j in range(0,len(der_hor), samples_per_trial):
		plt.axvline(x=j, color='tab:gray', linestyle=':')
	plt.show()


def movement_plot(trial_hor, trial_ver, trial_lab, movement):
	"""
# FUNCTION:	 	movement_plot(trial_hor, trial_ver, trial_lab, movement)
# INPUT: 		Horizontal & Vertical components of each trial, its labels
#				& the movement to be shown
# OUTPUT: 		Lineplot
# DESCRIPTION:	Generate the plots for horizontal and vertical values and
#				shows the division over samples corresponding to the desired movement
	"""

	hor = []
	ver = []

	samples_per_trial = global_variables.get_samples_per_trial()

	for i in range(0, len(trial_lab)):
		if trial_lab[i] == movement:
			for j in range(0, len(trial_hor[i])):
				hor.append(trial_hor[i][j]/8)
				ver.append(trial_ver[i][j]/8)

	plt.subplot(211)
	plt.plot(range(0, len(ver)), ver)
	plt.title(movement+" Ver")
#	plt.xticks(np.arange(250,len(hor)+250, step=samples_per_trial),movement, rotation=45, fontsize = 8)
	plt.xticks(np.arange(0,len(hor), step=samples_per_trial),[], rotation=45, fontsize = 8)
	for j in range(0,len(ver), samples_per_trial):
		plt.axvline(x=j, color='tab:gray', linestyle=':')
	
	plt.subplot(212)
	plt.plot(range(0, len(hor)), hor)
	plt.title(movement+" Hor")
#	plt.xticks(np.arange(250,len(hor)+250, step=samples_per_trial),movement, rotation=45, fontsize = 8)
	plt.xticks(np.arange(0,len(hor), step=samples_per_trial),[], rotation=45, fontsize = 8)
	
	for j in range(0,len(hor), samples_per_trial):
		plt.axvline(x=j, color='tab:gray', linestyle=':')
	plt.show()


def feature_plot(feat, trial_lab):
	"""
# FUNCTION:	 	feature_plot(feat, to_plot)
# INPUT: 		Matrix with the features and array with sample labels
# OUTPUT: 		Boxplot
# DESCRIPTION:	Creates a boxplot with a box for all values of the desired feature
#				splited into movements and horizontal & vertical components
	"""
	
	up_hor_min_feat = []
	up_hor_max_feat = []		
	up_hor_median_feat = []		
	up_ver_min_feat = []
	up_ver_max_feat = []
	up_ver_median_feat = []
	
	down_hor_min_feat = []
	down_hor_max_feat	= []
	down_hor_median_feat	= []		
	down_ver_min_feat = []
	down_ver_max_feat = []
	down_ver_median_feat = []
	
	left_hor_min_feat = []
	left_hor_max_feat = []
	left_hor_median_feat	= []	
	left_ver_min_feat = []
	left_ver_max_feat = []
	left_ver_median_feat = []
	
	right_hor_min_feat = []
	right_hor_max_feat = []			
	right_hor_median_feat = []	
	right_ver_min_feat = []
	right_ver_max_feat = []
	right_ver_median_feat = []
	
	for iter in range(0, len(trial_lab)):
		if trial_lab[iter] == "'Up'":
			up_hor_min_feat.append(feat[iter][0]/8)
			up_hor_max_feat.append(feat[iter][1]/8)			
			up_hor_median_feat.append(feat[iter][2]/8)			
			up_ver_min_feat.append(feat[iter][3]/8)
			up_ver_max_feat.append(feat[iter][4]/8)
			up_ver_median_feat.append(feat[iter][5]/8)
		elif trial_lab[iter] == "'Down'":
			down_hor_min_feat.append(feat[iter][0]/8)
			down_hor_max_feat.append(feat[iter][1]/8)			
			down_hor_median_feat.append(feat[iter][2]/8)			
			down_ver_min_feat.append(feat[iter][3]/8)
			down_ver_max_feat.append(feat[iter][4]/8)
			down_ver_median_feat.append(feat[iter][5]/8)
		elif trial_lab[iter] == "'Left'":
			left_hor_min_feat.append(feat[iter][0]/8)
			left_hor_max_feat.append(feat[iter][1]/8)			
			left_hor_median_feat.append(feat[iter][2]/8)			
			left_ver_min_feat.append(feat[iter][3]/8)
			left_ver_max_feat.append(feat[iter][4]/8)
			left_ver_median_feat.append(feat[iter][5]/8)
		elif trial_lab[iter] == "'Right'":
			right_hor_min_feat.append(feat[iter][0]/8)
			right_hor_max_feat.append(feat[iter][1]/8)			
			right_hor_median_feat.append(feat[iter][2]/8)			
			right_ver_min_feat.append(feat[iter][3]/8)
			right_ver_max_feat.append(feat[iter][4]/8)
			right_ver_median_feat.append(feat[iter][5]/8)

	data_hor_min = [up_hor_min_feat,down_hor_min_feat,left_hor_min_feat,right_hor_min_feat]
	data_hor_max = [up_hor_max_feat,down_hor_max_feat,left_hor_max_feat,right_hor_max_feat]
	data_hor_median = [up_hor_median_feat,down_hor_median_feat,left_hor_median_feat,right_hor_median_feat]

	data_ver_min = [up_ver_min_feat,down_ver_min_feat,left_ver_min_feat,right_ver_min_feat]
	data_ver_max = [up_ver_max_feat,down_ver_max_feat,left_ver_max_feat,right_ver_max_feat]
	data_ver_median = [up_ver_median_feat,down_ver_median_feat,left_ver_median_feat,right_ver_median_feat]

	plot_hor_labels = ['Up','Down','Left','Right']
	plot_ver_labels = ['Up','Down','Left','Right']

	fig = plt.figure()
	ax1 = fig.add_subplot(231)
	ax1.boxplot(data_hor_min)
	ax1.set_xticklabels(plot_hor_labels)
	ax1.set_ylabel('mV')
	ax1.set_title('Horizontal Min')
	
	ax2 = fig.add_subplot(232)
	ax2.boxplot(data_hor_max)
	ax2.set_xticklabels(plot_hor_labels)
	ax2.set_title('Horizontal Max')
	
	ax3 = fig.add_subplot(233)
	ax3.boxplot(data_hor_median)
	ax3.set_xticklabels(plot_hor_labels)
	ax3.set_title('Horizontal Median')
	
	ax4 = fig.add_subplot(234)
	ax4.boxplot(data_ver_min)
	ax4.set_xticklabels(plot_hor_labels)
	ax4.set_ylabel('mV')
	ax4.set_title('Vertical Min')
	
	ax5 = fig.add_subplot(235)
	ax5.boxplot(data_ver_max)
	ax5.set_xticklabels(plot_hor_labels)
	ax5.set_title('Vertical Max')
	
	ax6 = fig.add_subplot(236)
	ax6.boxplot(data_ver_median)
	ax6.set_xticklabels(plot_hor_labels)
	ax6.set_title('Vertical Median')

	plt.show()

	

def feature3d_plot(feat, trial_lab):
	"""
# FUNCTION:	 	feature_plot(feat, to_plot)
# INPUT: 		Matrix with the features, array with sample labels and 
#				the name of the feature to plot
# OUTPUT: 		Boxplot
# DESCRIPTION:	Creates a boxplot with a box for all values of the desired feature
#				splited into movements and horizontal & vertical components
	"""
	
	up_hor_min_feat = []
	up_hor_max_feat = []		
	up_hor_median_feat = []		
	up_ver_min_feat = []
	up_ver_max_feat = []
	up_ver_median_feat = []
	
	down_hor_min_feat = []
	down_hor_max_feat	= []
	down_hor_median_feat	= []		
	down_ver_min_feat = []
	down_ver_max_feat = []
	down_ver_median_feat = []
	
	left_hor_min_feat = []
	left_hor_max_feat = []
	left_hor_median_feat	= []	
	left_ver_min_feat = []
	left_ver_max_feat = []
	left_ver_median_feat = []
	
	right_hor_min_feat = []
	right_hor_max_feat = []			
	right_hor_median_feat = []	
	right_ver_min_feat = []
	right_ver_max_feat = []
	right_ver_median_feat = []
	
	for iter in range(0, len(trial_lab)):
		if trial_lab[iter] == "'Up'":
			up_hor_min_feat.append(feat[iter][0])
			up_hor_max_feat.append(feat[iter][1])			
			up_hor_median_feat.append(feat[iter][2])			
			up_ver_min_feat.append(feat[iter][3])
			up_ver_max_feat.append(feat[iter][4])
			up_ver_median_feat.append(feat[iter][5])
		elif trial_lab[iter] == "'Down'":
			down_hor_min_feat.append(feat[iter][0])
			down_hor_max_feat.append(feat[iter][1])			
			down_hor_median_feat.append(feat[iter][2])			
			down_ver_min_feat.append(feat[iter][3])
			down_ver_max_feat.append(feat[iter][4])
			down_ver_median_feat.append(feat[iter][5])
		elif trial_lab[iter] == "'Left'":
			left_hor_min_feat.append(feat[iter][0])
			left_hor_max_feat.append(feat[iter][1])			
			left_hor_median_feat.append(feat[iter][2])			
			left_ver_min_feat.append(feat[iter][3])
			left_ver_max_feat.append(feat[iter][4])
			left_ver_median_feat.append(feat[iter][5])
		elif trial_lab[iter] == "'Right'":
			right_hor_min_feat.append(feat[iter][0])
			right_hor_max_feat.append(feat[iter][1])			
			right_hor_median_feat.append(feat[iter][2])			
			right_ver_min_feat.append(feat[iter][3])
			right_ver_max_feat.append(feat[iter][4])
			right_ver_median_feat.append(feat[iter][5])
	
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(up_hor_min_feat, up_hor_max_feat, up_hor_median_feat, color='r', label='Up')
	ax.scatter(down_hor_min_feat, down_hor_max_feat, down_hor_median_feat, color='g', label='Down')
	ax.scatter(left_hor_min_feat, left_hor_max_feat, left_hor_median_feat, color='b', label='Left')
	ax.scatter(right_hor_min_feat, right_hor_max_feat, right_hor_median_feat, color='y', label='Right')
	ax.set_xlabel('Min')
	ax.set_ylabel('Max')
	ax.set_zlabel('Median')
	leg = ax.legend(loc='lower left')
	ax.set_title("Horizontal")
	fig2 = plt.figure()
	ax2 = fig2.add_subplot(111, projection='3d')
	ax2.scatter(up_ver_min_feat, up_ver_max_feat, up_ver_median_feat, color='r', label='Up')
	ax2.scatter(down_ver_min_feat, down_ver_max_feat, down_ver_median_feat, color='g', label='Down')
	ax2.scatter(left_ver_min_feat, left_ver_max_feat, left_ver_median_feat, color='b', label='Left')
	ax2.scatter(right_ver_min_feat, right_ver_max_feat, right_ver_median_feat, color='y', label='Right')
	ax2.set_xlabel('Min')
	ax2.set_ylabel('Max')
	ax2.set_zlabel('Median')
	leg2 = ax2.legend(loc='lower left')
	ax2.set_title("Vertical")
	plt.show()
	
	
def feature2d_plot(feat, trial_lab):

	up_hor_min_feat = []
	up_hor_max_feat = []		
	up_hor_median_feat = []		
	up_ver_min_feat = []
	up_ver_max_feat = []
	up_ver_median_feat = []
	
	down_hor_min_feat = []
	down_hor_max_feat	= []
	down_hor_median_feat	= []		
	down_ver_min_feat = []
	down_ver_max_feat = []
	down_ver_median_feat = []
	
	left_hor_min_feat = []
	left_hor_max_feat = []
	left_hor_median_feat	= []	
	left_ver_min_feat = []
	left_ver_max_feat = []
	left_ver_median_feat = []
	
	right_hor_min_feat = []
	right_hor_max_feat = []			
	right_hor_median_feat = []	
	right_ver_min_feat = []
	right_ver_max_feat = []
	right_ver_median_feat = []
	
	for iter in range(0, len(trial_lab)):
		if trial_lab[iter] == "'Up'":
			up_hor_min_feat.append(feat[iter][0]/8)
			up_hor_max_feat.append(feat[iter][1]/8)			
			up_hor_median_feat.append(feat[iter][2]/8)			
			up_ver_min_feat.append(feat[iter][3]/8)
			up_ver_max_feat.append(feat[iter][4]/8)
			up_ver_median_feat.append(feat[iter][5]/8)
		elif trial_lab[iter] == "'Down'":
			down_hor_min_feat.append(feat[iter][0]/8)
			down_hor_max_feat.append(feat[iter][1]/8)			
			down_hor_median_feat.append(feat[iter][2]/8)			
			down_ver_min_feat.append(feat[iter][3]/8)
			down_ver_max_feat.append(feat[iter][4]/8)
			down_ver_median_feat.append(feat[iter][5]/8)
		elif trial_lab[iter] == "'Left'":
			left_hor_min_feat.append(feat[iter][0]/8)
			left_hor_max_feat.append(feat[iter][1]/8)			
			left_hor_median_feat.append(feat[iter][2]/8)			
			left_ver_min_feat.append(feat[iter][3]/8)
			left_ver_max_feat.append(feat[iter][4]/8)
			left_ver_median_feat.append(feat[iter][5]/8)
		elif trial_lab[iter] == "'Right'":
			right_hor_min_feat.append(feat[iter][0]/8)
			right_hor_max_feat.append(feat[iter][1]/8)			
			right_hor_median_feat.append(feat[iter][2]/8)			
			right_ver_min_feat.append(feat[iter][3]/8)
			right_ver_max_feat.append(feat[iter][4]/8)
			right_ver_median_feat.append(feat[iter][5]/8)

	fig = plt.figure()
	ax1 = fig.add_subplot(231)
	ax1.scatter(up_hor_min_feat, up_hor_max_feat, marker = ".", color='r', label='Up')
	ax1.scatter(down_hor_min_feat, down_hor_max_feat, marker = "v", color='g', label='Down')
	ax1.scatter(left_hor_min_feat, left_hor_max_feat, marker = "s", color='b', label='Left')
	ax1.scatter(right_hor_min_feat, right_hor_max_feat, marker = "x", color='y', label='Right')
	ax1.set_xlabel('Min (mV)')
	ax1.set_ylabel('Max (mV)')
	
	ax2 = fig.add_subplot(232)
	ax2.scatter(up_hor_max_feat, up_hor_median_feat, marker = ".", color='r', label='Up')
	ax2.scatter(down_hor_max_feat, down_hor_median_feat, marker = "v", color='g', label='Down')
	ax2.scatter(left_hor_max_feat, left_hor_median_feat, marker = "s", color='b', label='Left')
	ax2.scatter(right_hor_max_feat, right_hor_median_feat, marker = "x", color='y', label='Right')
	ax2.set_xlabel('Max (mV)')
	ax2.set_ylabel('Median (mV)')
	ax2.set_title('Horizontal')
	
	ax3 = fig.add_subplot(233)
	ax3.scatter(up_hor_median_feat, up_hor_min_feat, marker = ".", color='r', label='Up')
	ax3.scatter(down_hor_median_feat, down_hor_min_feat, marker = "v", color='g', label='Down')
	ax3.scatter(left_hor_median_feat, left_hor_min_feat, marker = "s", color='b', label='Left')
	ax3.scatter(right_hor_median_feat, right_hor_min_feat, marker = "x", color='y', label='Right')
	ax3.set_xlabel('Median (mV)')
	ax3.set_ylabel('Min (mV)')
	ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	
	ax4 = fig.add_subplot(234)
	ax4.scatter(up_ver_min_feat, up_ver_max_feat, marker = ".", color='r', label='Up')
	ax4.scatter(down_ver_min_feat, down_ver_max_feat, marker = "v", color='g', label='Down')
	ax4.scatter(left_ver_min_feat, left_ver_max_feat, marker = "s", color='b', label='Left')
	ax4.scatter(right_ver_min_feat, right_ver_max_feat, marker = "x", color='y', label='Right')
	ax4.set_xlabel('Min (mV)')
	ax4.set_ylabel('Max (mV)')
	
	ax5 = fig.add_subplot(235)
	ax5.scatter(up_ver_max_feat, up_ver_median_feat, marker = ".", color='r', label='Up')
	ax5.scatter(down_ver_max_feat, down_ver_median_feat, marker = "v", color='g', label='Down')
	ax5.scatter(left_ver_max_feat, left_ver_median_feat, marker = "s", color='b', label='Left')
	ax5.scatter(right_ver_max_feat, right_ver_median_feat, marker = "x", color='y', label='Right')
	ax5.set_xlabel('Max (mV)')
	ax5.set_ylabel('Median (mV)')
	ax5.set_title('Vertical')
	
	ax6 = fig.add_subplot(236)
	ax6.scatter(up_ver_median_feat, up_ver_min_feat, marker = ".", color='r', label='Up')
	ax6.scatter(down_ver_median_feat, down_ver_min_feat, marker = "v", color='g', label='Down')
	ax6.scatter(left_ver_median_feat, left_ver_min_feat, marker = "s", color='b', label='Left')
	ax6.scatter(right_ver_median_feat, right_ver_min_feat, marker = "x", color='y', label='Right')
	ax6.set_xlabel('Median (mV)')
	ax6.set_ylabel('Min (mV)')

	plt.show()



def old_feature_plot(feat, trial_lab, to_plot):
	"""
# FUNCTION:	 	feature_plot(feat, to_plot)
# INPUT: 		Matrix with the features, array with sample labels and 
#				the name of the feature to plot
# OUTPUT: 		Boxplot
# DESCRIPTION:	Creates a boxplot with a box for all values of the desired feature
#				splited into movements and horizontal & vertical components
	"""
	
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

	plot_labels = ["Up Hor","Down Hor","Left Hor","Right Hor","Up Ver","Down Ver","Left Ver","Right Ver"]
	ax.set_xticklabels(plot_labels)
	ax.set_title(to_plot)
	#plt.yticks(np.arange(-1,1))

	ax.boxplot(data)
	plt.show()
	

def derivative_plots(trial_hor, trial_ver, trial_lab):

	up_hor_amp = []
	up_ver_amp = []
	up_hor_min = []
	up_ver_min = []
	up_hor_max = []
	up_ver_max = []
	up_hor_median = []
	up_ver_median = []
	up_hor_sum = []
	up_ver_sum = []
	up_tot_sum = []
	
	down_hor_amp = []
	down_ver_amp = []
	down_hor_min = []
	down_ver_min = []
	down_hor_max = []
	down_ver_max = []
	down_hor_median = []
	down_ver_median = []
	down_hor_sum = []
	down_ver_sum = []
	down_tot_sum = []
	
	left_hor_amp = []
	left_ver_amp = []
	left_hor_min = []
	left_ver_min = []
	left_hor_max = []
	left_ver_max = []
	left_hor_median = []
	left_ver_median = []
	left_hor_sum = []
	left_ver_sum = []
	left_tot_sum = []
	
	right_hor_amp = []
	right_ver_amp = []
	right_hor_min = []
	right_ver_min = []
	right_hor_max = []
	right_ver_max = []
	right_hor_median = []
	right_ver_median = []
	right_hor_sum = []
	right_ver_sum = []
	right_tot_sum = []

	none_hor_amp = []
	none_ver_amp = []
	none_hor_min = []
	none_ver_min = []
	none_hor_max = []
	none_ver_max = []
	none_hor_median = []
	none_ver_median = []
	none_hor_sum = []
	none_ver_sum = []
	none_tot_sum = []

	blink_hor_amp = []
	blink_ver_amp = []
	blink_hor_min = []
	blink_ver_min = []
	blink_hor_max = []
	blink_ver_max = []
	blink_hor_median = []
	blink_ver_median = []
	blink_hor_sum = []
	blink_ver_sum = []
	blink_tot_sum = []

	close_hor_amp = []
	close_ver_amp = []
	close_hor_min = []
	close_ver_min = []
	close_hor_max = []
	close_ver_max = []
	close_hor_median = []
	close_ver_median = []
	close_hor_sum = []
	close_ver_sum = []
	close_tot_sum = []

	der_hor = []
	der_ver = []

	amp_hor = []
	amp_ver = []

	sum_hor = []
	sum_ver = []

	amp_up = []
	amp_down = []
	amp_left = []
	amp_right = []
	amp_none = []
	amp_blink = []
	amp_close = []

	for i in range(0, len(trial_hor)):
		hor = []
		ver = []
		for j in range(0, len(trial_hor[i])):
				hor.append(trial_hor[i][j])
				ver.append(trial_ver[i][j])
		der_hor.extend(np.gradient(hor,5))
		der_ver.extend(np.gradient(ver,5))

	samples_per_trial = global_variables.get_samples_per_trial()
	split_indx = range(samples_per_trial, len(der_hor), samples_per_trial)
	der_hor = np.split(der_hor, split_indx)
	der_ver = np.split(der_ver, split_indx)

	for j in range(0, len(trial_hor)):
		amp_hor.append(np.max(der_hor[j]) - np.min(der_hor[j]))
		amp_ver.append(np.max(der_ver[j]) - np.min(der_ver[j]))
		sum_hor.append(sum(abs(der_hor[j])))
		sum_ver.append(sum(abs(der_ver[j])))


	for iter in range(0, len(trial_lab)):
		if trial_lab[iter] == "'Up'":
			up_hor_amp.append(amp_hor[iter])
			up_ver_amp.append(amp_ver[iter])
			up_hor_min.append(np.min(der_hor[iter]))
			up_ver_min.append(np.min(der_ver[iter]))
			up_hor_max.append(np.max(der_hor[iter]))
			up_ver_max.append(np.max(der_ver[iter]))
			up_hor_median.append(np.median(der_hor[iter]))
			up_ver_median.append(np.median(der_ver[iter]))
			amp_up.append(amp_hor[iter]+amp_ver[iter])
			up_hor_sum.append(sum_hor[iter])
			up_ver_sum.append(sum_ver[iter])
			up_tot_sum.append(sum_hor[iter]+sum_ver[iter]) 
		elif trial_lab[iter] == "'Down'":
			down_hor_amp.append(amp_hor[iter])
			down_ver_amp.append(amp_ver[iter])
			down_hor_min.append(np.min(der_hor[iter]))
			down_ver_min.append(np.min(der_ver[iter]))
			down_hor_max.append(np.max(der_hor[iter]))
			down_ver_max.append(np.max(der_ver[iter]))
			down_hor_median.append(np.median(der_hor[iter]))
			down_ver_median.append(np.median(der_ver[iter]))
			amp_down.append(amp_hor[iter]+amp_ver[iter])
			down_hor_sum.append(sum_hor[iter])
			down_ver_sum.append(sum_ver[iter])
			down_tot_sum.append(sum_hor[iter]+sum_ver[iter]) 
		elif trial_lab[iter] == "'Left'":
			left_hor_amp.append(amp_hor[iter])
			left_ver_amp.append(amp_ver[iter])
			left_hor_min.append(np.min(der_hor[iter]))
			left_ver_min.append(np.min(der_ver[iter]))
			left_hor_max.append(np.max(der_hor[iter]))
			left_ver_max.append(np.max(der_ver[iter]))
			left_hor_median.append(np.median(der_hor[iter]))
			left_ver_median.append(np.median(der_ver[iter]))
			amp_left.append(amp_hor[iter]+amp_ver[iter])
			left_hor_sum.append(sum_hor[iter])
			left_ver_sum.append(sum_ver[iter])
			left_tot_sum.append(sum_hor[iter]+sum_ver[iter]) 
		elif trial_lab[iter] == "'Right'":
			right_hor_amp.append(amp_hor[iter])
			right_ver_amp.append(amp_ver[iter])
			right_hor_min.append(np.min(der_hor[iter]))
			right_ver_min.append(np.min(der_ver[iter]))
			right_hor_max.append(np.max(der_hor[iter]))
			right_ver_max.append(np.max(der_ver[iter]))
			right_hor_median.append(np.median(der_hor[iter]))
			right_ver_median.append(np.median(der_ver[iter]))
			amp_right.append(amp_hor[iter]+amp_ver[iter])
			right_hor_sum.append(sum_hor[iter])
			right_ver_sum.append(sum_ver[iter])
			right_tot_sum.append(sum_hor[iter]+sum_ver[iter]) 
		elif trial_lab[iter] == "'None'" or trial_lab[iter] == "'No_Movement'":
			none_hor_amp.append(amp_hor[iter])
			none_ver_amp.append(amp_ver[iter])
			none_hor_min.append(np.min(der_hor[iter]))
			none_ver_min.append(np.min(der_ver[iter]))
			none_hor_max.append(np.max(der_hor[iter]))
			none_ver_max.append(np.max(der_ver[iter]))
			none_hor_median.append(np.median(der_hor[iter]))
			none_ver_median.append(np.median(der_ver[iter]))
			amp_none.append(amp_hor[iter]+amp_ver[iter])
			none_hor_sum.append(sum_hor[iter])
			none_ver_sum.append(sum_ver[iter])
			none_tot_sum.append(sum_hor[iter]+sum_ver[iter]) 
		elif trial_lab[iter] == "'Blink'":
			blink_hor_amp.append(amp_hor[iter])
			blink_ver_amp.append(amp_ver[iter])
			blink_hor_min.append(np.min(der_hor[iter]))
			blink_ver_min.append(np.min(der_ver[iter]))
			blink_hor_max.append(np.max(der_hor[iter]))
			blink_ver_max.append(np.max(der_ver[iter]))
			blink_hor_median.append(np.median(der_hor[iter]))
			blink_ver_median.append(np.median(der_ver[iter]))
			amp_blink.append(amp_hor[iter]+amp_ver[iter])
			blink_hor_sum.append(sum_hor[iter])
			blink_ver_sum.append(sum_ver[iter])
			blink_tot_sum.append(sum_hor[iter]+sum_ver[iter]) 
		elif trial_lab[iter] == "'Close_Eyes'":
			close_hor_amp.append(amp_hor[iter])
			close_ver_amp.append(amp_ver[iter])
			close_hor_min.append(np.min(der_hor[iter]))
			close_ver_min.append(np.min(der_ver[iter]))
			close_hor_max.append(np.max(der_hor[iter]))
			close_ver_max.append(np.max(der_ver[iter]))
			close_hor_median.append(np.median(der_hor[iter]))
			close_ver_median.append(np.median(der_ver[iter]))
			amp_close.append(amp_hor[iter]+amp_ver[iter])
			close_hor_sum.append(sum_hor[iter])
			close_ver_sum.append(sum_ver[iter])
			close_tot_sum.append(sum_hor[iter]+sum_ver[iter]) 

	data_hor = [up_hor_amp, down_hor_amp, left_hor_amp, right_hor_amp, none_hor_amp, blink_hor_amp, close_hor_amp]
	data_ver = [up_ver_amp, down_ver_amp, left_ver_amp, right_ver_amp, none_ver_amp, blink_ver_amp, close_ver_amp]
	data_total = [amp_up, amp_down, amp_left, amp_right, amp_none, amp_blink, amp_close]
	data_hor_sum = [up_hor_sum, down_hor_sum, left_hor_sum, right_hor_sum, none_hor_sum, blink_hor_sum, close_hor_sum]
	data_ver_sum = [up_ver_sum, down_ver_sum, left_ver_sum, right_ver_sum, none_ver_sum, blink_ver_sum, close_ver_sum]
	data_tot_sum = [up_tot_sum, down_tot_sum, left_tot_sum, right_tot_sum, none_tot_sum, blink_tot_sum, close_tot_sum]
	plot_labels = ["Up", "Down", "Left", "Right", "None", "Blink", "Closed"]


	plt.figure(1)
	ax = plt.gca()
	ticks = ax.get_xticklabels()
	ax.boxplot(data_hor)
	ax.set_xticklabels(plot_labels, rotation = 45, fontsize = 8)
	ax.set_title("Horizontal Derivative Amplitude")

	plt.figure(2)
	ax = plt.gca()
	ticks = ax.get_xticklabels()
	ax.boxplot(data_ver)
	ax.set_xticklabels(plot_labels, rotation = 45, fontsize = 8)
	ax.set_title("Vertical Derivative Amplitude")

	plt.figure(3)
	ax = plt.gca()
	ticks = ax.get_xticklabels()
	ax.boxplot(data_total)
	ax.set_xticklabels(plot_labels, rotation = 45, fontsize = 8)
	ax.set_title("Total (Hor+Ver) Derivative Amplitude")

	plt.figure(4)
	ax = plt.gca()
	ticks = ax.get_xticklabels()
	ax.boxplot(data_hor_sum)
	ax.set_xticklabels(plot_labels, rotation = 45, fontsize = 8)
	ax.set_title("Derivative Horizontal Sum")

	plt.figure(5)
	ax = plt.gca()
	ticks = ax.get_xticklabels()
	ax.boxplot(data_ver_sum)
	ax.set_xticklabels(plot_labels, rotation = 45, fontsize = 8)
	ax.set_title("Derivative Vertical Sum")

	plt.figure(6)
	ax = plt.gca()
	ticks = ax.get_xticklabels()
	ax.boxplot(data_tot_sum)
	ax.set_xticklabels(plot_labels, rotation = 45, fontsize = 8)
	ax.set_title("Derivative Vertical+Horizontal Sum")

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(up_hor_min, up_hor_max, up_hor_amp, color='r', label='Up')
	ax.scatter(down_hor_min, down_hor_max, down_hor_amp, color='r', label='Down')
	ax.scatter(left_hor_min, left_hor_max, left_hor_amp, color='g', label='Left')
	ax.scatter(right_hor_min, right_hor_max, right_hor_amp, color='g', label='Right')
	ax.scatter(none_hor_min, none_hor_max, none_hor_amp, color='k', label='No Movement')
	ax.scatter(blink_hor_min, blink_hor_max, blink_hor_amp, color='c', label='Blink')
	ax.scatter(close_hor_min, close_hor_max, close_hor_amp, color='w', label='Closed')
	ax.set_xlabel('Derivative Min')
	ax.set_ylabel('Derivative Max')
	ax.set_zlabel('Derivative Amplitude')
	leg = ax.legend(loc='lower left')
	ax.set_title("Horizontal")
	fig2 = plt.figure()
	ax2 = fig2.add_subplot(111, projection='3d')
	ax2.scatter(up_ver_min, up_ver_max, up_ver_amp, color='g', label='Up')
	ax2.scatter(down_ver_min, down_ver_max, down_ver_amp, color='g', label='Down')
	ax2.scatter(left_ver_min, left_ver_max, left_ver_amp, color='r', label='Left')
	ax2.scatter(right_ver_min, right_ver_max, right_ver_amp, color='r', label='Right')
	ax2.scatter(none_ver_min, none_ver_max, none_ver_amp, color='k', label='No Movement')
	ax2.scatter(blink_ver_min, blink_ver_max, blink_ver_amp, color='c', label='Blink')
	ax2.scatter(close_ver_min, close_ver_max, close_ver_amp, color='w', label='Closed')
	ax2.set_xlabel('Derivative Min')
	ax2.set_ylabel('Derivative Max')
	ax2.set_zlabel('Derivative Amplitude')
	leg2 = ax2.legend(loc='lower left')
	ax2.set_title("Vertical")
	
	plt.show()