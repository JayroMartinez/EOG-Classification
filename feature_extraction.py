#	HERE WE CALCULATE THE FEATURES FOR THE DATA
#	AUTHOR: Jayro Martinez Cervero

import numpy as np
from scipy import stats

import plots

def features(trial_hor, trial_ver):
	"""
# FUNCTION:	 	features(trial_hor, trial_ver)
# INPUT: 		Horizontal & Vertical components of each trial
# OUTPUT: 		Matrix with feature values of horizontal & vertical
#				components of each trial
# DESCRIPTION:	Extracts the features for each trial
# AUTHOR:		Jayro Martinez-Cervero
	"""

	num_feat = 6
	features = np.zeros((len(trial_hor), num_feat))
	
	for iter in range(0, len(trial_hor)):
		
		features[iter][0] = np.min(trial_hor[iter]) 	# Horizontal Min 
		features[iter][1] = np.max(trial_hor[iter]) 	# Horizontal Max
		features[iter][2] = np.median(trial_hor[iter])	# Horizontal Median

		features[iter][3] = np.min(trial_ver[iter]) 	# Vertical Min
		features[iter][4] = np.max(trial_ver[iter]) 	# Vertical Max
		features[iter][5] = np.median(trial_ver[iter]) 	# Vertical Median
		
	return features