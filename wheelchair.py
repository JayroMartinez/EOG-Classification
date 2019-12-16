import time
from datetime import datetime
import pickle
import sys
import os
from natsort import natsorted
import glob

import connect_acquire_store as con
import filter_files as filt
import feature_extraction as feat
import svm_classification as classif
import online_classification as online
import plots
import global_variables

def menu():

	os.system('clear')

	# We show the main menu
	print("*******************************************************")
	print("*******************************************************")
	print("*********                                     *********")
	print("***   WELCOME TO OUR FANTASTIC WHEELCHAIR PROGRAM   ***")
	print("*********                                     *********")
	print("*******************************************************")
	print("*******************************************************")
	print("\nYou can perform the following actions:\n")
	print("	1. Acquire New Data")
	print("	2. Pre-process Data, Extract Features & Classify")
	print("	3. Online Classification")
	print("	0. EXIT\n")
	
	option = input("What would you like to do?: ")

	if option == '1': # Acquire new data

		os.system('clear')
		files_in_data = [x for x in os.listdir('./data') if x.endswith(".txt")]
		files_in_data = natsorted(files_in_data)
		print("Select the file to save the new data: \n")
		print("	 0 : Create a New File")
		for i in range(0,len(files_in_data)): 
			print("	",i+1, ": Add to File ", files_in_data[i])
		target_file = int(input("\nYour selection: "))
		if target_file == 0:
			os.system('clear')
			file_name = input("Please write the name of the file (without extension): ")
			global_variables.set_save_file(file_name+".txt")
		elif target_file <= len(files_in_data):
			file_name = files_in_data[target_file-1]	
			global_variables.set_save_file(file_name)
		else:
			os.system('clear')
			print("Wrong Option, sorry.")
			time.sleep(2)
			menu()

# Connection, Data Acquisition & Data Storage
		con.connect()

	elif option == '2': # Pre-process data, extract features & classify
		
		os.system('clear')
		all_files = []
		files_to_process = []
		all_files = [x for x in os.listdir('./data') if x.endswith(".txt")]
		all_files = natsorted(all_files)
		print("Select the file/s to pre-process\n")
		
		for i in range(0, len(all_files)):
			print("	", i, " : ", all_files[i])
			
		selected_files = input("\nSelect desired files (you can use '-' to select ranges and/or ',' to select multiple datasets): ")
		selected_files = selected_files.split(',')
		aux = []
			
		for j in range(0, len(selected_files)):
			aux = selected_files[j].split('-')
				
			for k in range(int(aux[0]), int(aux[-1])+1):

				files_to_process.append("./data/"+all_files[k])
		

		global_variables.set_files_to_process(files_to_process)

		time.sleep(1)
		os.system('clear')

		# Data Load, Filtering & Trial Split
		print("Pre-processing & extracting features from files : ", files_to_process)
	
		trial_hor, trial_ver, trial_lab = filt.filter()

		# Feature Extraction
		features = []
		features = feat.features(trial_hor, trial_ver)

		#plots.trial_plot(trial_hor, trial_ver)
		#plots.feature_plot(features, trial_lab, "Derivative Slope")

		print("\nPre-processing & Feature extraction done. Now we are going to perform classification.")
		
		# Classification
		classif.classification(features, trial_lab)
	
		save = input("\nDo you want to save the model?? [y/n]: ")
		if save == 'y' or save == 'Y':
			model_name = input("Write model name: ")
			model_file_name = "./models/"+model_name+".sav"
			model = global_variables.get_model()
			pickle.dump(model, open(model_file_name, 'wb'))
			print("Model saved in "+model_file_name)

		time.sleep(3)	
		menu()

	elif option == '3': # Online classification

		models_list = []
		models_list = [x for x in os.listdir('./models') if x.endswith(".sav")]
		models_list = natsorted(models_list)
		os.system('clear')
		print("Available models:\n")
		
		for l in range(0, len(models_list)):
			print("	", l, " : ", models_list[l])

		model = input("\nSelect the model for classification: ")
		global_variables.set_model(models_list[int(model)])
		os.system('clear')
		print("Online classification started. \nModel selected: ", global_variables.get_model(), "\n")

		# Online Classification	
		online.online_classif()

	elif option == '0': # EXIT
		os.system('clear')
		print("###############################")
		print("##     SEE YOU SOON!!!!!!    ##")
		print("###############################")
		time.sleep(3)
		os.system('clear')
		sys.exit()

	else: # Wrong option
		print("\nYou selected a wrong option. ARE YOU KIDDING ME?")
		time.sleep(2)
		menu()

	
if __name__ == '__main__':

	files_to_process = global_variables.get_files_to_process()
	samples_per_trial = global_variables.get_samples_per_trial()
	sample_rate = global_variables.get_sample_rate()

	menu()




	







	
