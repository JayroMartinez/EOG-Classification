####################################################################
####################################################################

## PROBABLEMENTE FUNCION INUTIL

####################################################################
####################################################################

import pickle
from sklearn.svm import SVC
import numpy as np


def online_test(features, trial_lab):

	#model_name = '/Users/jayromartinez/Dropbox/OpenBCI/models/bloque6_9_acc892_3Feat.sav'
	model_name = '/home/pi/Desktop/OpenBCI/models/w1235_f003-30-10_acc95.sav'
	model = pickle.load(open(model_name, 'rb'))
	labels = ['Up', 'Down', 'Left', 'Right']

	aciertos = 0
	pseudo_aciertos = 0
	
	for i in range(0, len(features)):

		probs = model.predict_proba([features[i]])

		labels.sort()
		max_pos = int(np.where(probs[0] == np.amax(probs[0]))[0])
		predicted = "'"+labels[max_pos]+"'"

#		print("\nReal: ", trial_lab[i], ", Predicted: ", predicted)

		if predicted == trial_lab[i]:
			pseudo_aciertos += 1
#			print("Pseudoacierto")
			if np.amax(probs) > 0.5:
				aciertos +=1
#				print("Acierto")
#		else:
#			print("Ñau")

	print("\n\nPseudoHits: ", pseudo_aciertos, "out of ", len(features), ". ", round(pseudo_aciertos/len(features)*100,3),"%")
	print("Real Hits: ", aciertos, "out of ", len(features), ". ", round(aciertos/len(features)*100,3),"%")

	