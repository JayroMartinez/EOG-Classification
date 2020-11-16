# HERE WE PERFORM THE CALCULATIONS FOR THE OFFLINE PARADIGM
# AUTHOR: Jayro Martinez Cervero

from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import numpy as np

import global_variables

def classification(feat, trial_lab):
	"""
# FUNCTION:	 	feature_plot(feat, to_plot)
# INPUT: 		Matrix with the features, labels for the trials
# OUTPUT: 		Accuracy of the model
# DESCRIPTION:	Creates an SVM model using train data and gives the test data scores
# AUTHOR: 		Jayro Martinez Cervero
	"""

# Train model and predict labels
	c = 0.8
	kernel = 'rbf'
	gamma = 'scale'
	decision = 'ovo'
	
	features = []
	labels = []

# Split data into Up-Down-Left-Righ & Movement-No Movement
	for iter in range(0, len(trial_lab)):
		if trial_lab[iter] == "'Up'":
			labels.append(trial_lab[iter])
			features.append(feat[iter])
			
		elif trial_lab[iter] == "'Down'":
			labels.append(trial_lab[iter])
			features.append(feat[iter])
			
		elif trial_lab[iter] == "'Left'":
			labels.append(trial_lab[iter])
			features.append(feat[iter])
			
		elif trial_lab[iter] == "'Right'":
			labels.append(trial_lab[iter])
			features.append(feat[iter])
			

	print("\nClassification started. \n\n","      C: ", c, "\n       Decision strategy: ", decision, "\n       Kernel: ", kernel)

# Classify 
	clf = SVC(C=c, kernel=kernel, gamma=gamma, probability=True, decision_function_shape=decision)
	scores = cross_val_score(clf,features, labels, cv=5)
	round_scores = []
	for s in scores:
		round_scores.append(round(s, 3))

	msg = "\nModels Accuracies:\n"+str(round_scores)+"\nModels Mean Accuracy: "+str(round(scores.mean(),3))+"\n\nWait until we fit the model\n This can take a while"

	if global_variables.get_interface():
		from tkinter import messagebox

		print(msg)
		messagebox.showinfo("Model Accuracy Info", msg)
	else:
		print(msg)

	clf.fit(features, labels)
	global_variables.set_model(clf)

		