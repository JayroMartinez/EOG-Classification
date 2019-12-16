import numpy as np

import global_variables

def to_trials(hor, ver, lab):
	"""
# FUNCTION:	 	to_trials(hor, ver, lab)
# INPUT: 		Horizontal and Vertical components of each timepoint and its label & 
#				the number of samples per trial
# OUTPUT: 		Horizontal and Vertical components of trial and its label
# DESCRIPTION:	Splits the timpoints into samples taking into account sample rate
#				& length of each trial. For old datasets also removes the actions 
#				that we don't want to use in our system. After that it's doing 
#				standarization over each sample
	"""

	samples_per_trial = global_variables.get_samples_per_trial()

# Split intro trials
	split_indx = range(samples_per_trial, len(lab), samples_per_trial)
	trial_hor = np.split(hor, split_indx)
	trial_ver = np.split(ver, split_indx)
	trial_lab = np.split(lab, split_indx)

# Remove 'beep' trials

	tri = 0
	while tri<len(trial_lab):
		if (trial_lab[tri][0] == "'beep'"):
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
		
		for t in (range(0, len(trial_ver[s]))):
			trial_ver[s][t] = (trial_ver[s][t] - ver_mean) / ver_sd
			trial_hor[s][t] = (trial_hor[s][t] - hor_mean) / hor_sd
				

	return trial_hor, trial_ver, trial_lab
