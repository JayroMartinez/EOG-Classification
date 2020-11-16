#	HERE WE CREATE THE GRAPHICAL INTERFACE WITH THE APPROPIATE CALL TO THE PIPELINE FUNCTIONS
#	AUTHOR: Jayro Martinez Cervero

import tkinter as tk
import tkinter.filedialog as tkfiledialog
import time
from datetime import datetime
import pickle
import sys
import os
from natsort import natsorted
import glob
import numpy as np
import matplotlib
matplotlib.use('TkAgg')

import global_variables
import plots

class OnlineClassification:
	def __init__(self, master):	# CREATES THE ONLINE CLASSIFICATION GUI WINDOW
		self.master = master
		self.master.withdraw()
		self.onlineWdw = tk.Toplevel()
		self.master.title("EOG Online Classification")
		self.btnOnline = tk.Button(self.onlineWdw, text="Start", command= lambda: self.btnOnlinePushed())
		self.btnOnline.config(height = 2, width = 30)
		self.btnOnline.pack()
		self.onlineWdw.mainloop()

	def btnOnlinePushed(self):	# CALLS TO ONLINE CLASSIFICATION
		import online_classification as online
		from multiprocessing import Process
		import pseudo_online as pseudo

		if not global_variables.get_online_started():
			self.btnOnline.config(text="STOP")
			self.onlineWdw.update()
			global_variables.set_online_started(True)
			global_variables.set_cont(0)
			print("STARTED")
			self.new_process = Process(target=online.online_classif())
			self.new_process.start()
			
		else:
			global_variables.set_online_started(False)
			self.new_process.terminate()
			self.onlineWdw.destroy()


class SaveWindow:
	def __init__(self, master):	# CREATES THE SAVE MODEL GUI WINDOW
		
		self.master = master
		self.save_wdw = tk.Toplevel()
		self.master.title("Enter File Name")
		self.label = tk.Label(self.save_wdw, text="Enter Model Name: ")
		self.model_entry = tk.Entry(self.save_wdw)
		self.save_button = tk.Button(self.save_wdw, text="Save Model", command = lambda: self.btnSaveModelPushed(self.model_entry.get()))
		self.save_button.config(height = 2, width = 30)
		self.label.pack()
		self.model_entry.pack()
		self.save_button.pack()
		self.save_wdw.mainloop()


	def btnSaveModelPushed(self, model_name):	# SAVES THE MODEL

		import global_variables

		if model_name:
			model_file_name = "./models/"+model_name+".sav"
			model = global_variables.get_model()
			pickle.dump(model, open(model_file_name, 'wb'))
			self.save_wdw.destroy()
		else:
			pass


class AcquireNewFile:
	def __init__(self, master):	# CREATES THE ACQUISITION GUI WINDOW
		
		self.master = master
		self.top = tk.Toplevel()
		self.top.title("Enter File Name")
		self.label = tk.Label(self.top, text="Enter File Name: ")
		self.file_entry = tk.Entry(self.top)
		self.save_button = tk.Button(self.top, text="Acquire", command= lambda: self.btnSaveDataPushed(self.file_entry.get()))
		self.save_button.config(height = 2, width = 30)
		self.label.pack()
		self.file_entry.pack()
		self.save_button.pack()
		self.top.mainloop()


	def btnSaveDataPushed(self, file_name):	# CALLS TO CONNECTION FUNCTION AND SETS THE SAVING PARAMETERS
		
		import global_variables
		import connect_acquire_store as con
		
		if file_name:
			new_file_name = "./data/"+file_name+".txt"
			global_variables.set_save_file(new_file_name)
			newname = global_variables.get_save_file()
			print(newname)
			con.connect()
			self.top.destroy()		


class AcquireOldFile:
	def __init__(self, master):	# CALLS TO CONNECTION FUNCTION AND SETS THE SAVING PARAMETERS
		
		import global_variables
		import connect_acquire_store as con
		
		root = tk.Tk()
		root.withdraw()
		root.file_name = tkfiledialog.askopenfilename(parent = root, initialdir = "./data",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
		if root.file_name:
			global_variables.set_save_file(root.file_name)
			con.connect()
			root.destroy()



class AcquireWindow:
	def __init__(self, master):	# CREATES THE ACQUISITION GUI WINDOW

		self.master = master
		self.top = tk.Toplevel(self.master)
		self.top.title("Acquire New Data")
		self.btnNewData = tk.Button(self.top, text='Create a New Data File or Overwrite Old Data File', command=self.acquireNewFile)
		self.btnOldData = tk.Button(self.top, text='Append to Old Data File', command=self.acquireOldFile)
		self.btnNewData.config(height = 2, width = 40)
		self.btnOldData.config(height = 2, width = 40)
		self.btnNewData.pack()
		self.btnOldData.pack()


	def acquireNewFile(self):	# CALLS TO ACQUISITION FUNCTION
		
		newFileWdw = AcquireNewFile(self)
		

	def acquireOldFile(self):	# CALLS TO ACQUISITION FUNCTION

		oldFileWdw = AcquireOldFile(self)



class MainWindow:
	def __init__(self, master):	# CREATES THE MAIN GUI WINDOW
	
		self.master = master
		self.frame = tk.Frame(self.master)
		self.master.title("EOG Project")
		self.btnAcquire = tk.Button(self.master, text='Acquire New Data', command = self.btnAcquirePushed)
		self.btnPreprocess = tk.Button(self.master, text='Process, Extract Features & Classify', command = self.btnPreprocessPushed)
		self.btnOnline = tk.Button(self.master, text='Online Classification', command = self.btnOnlinePushed)
		self.btnAcquire.config(height = 2, width = 30)
		self.btnPreprocess.config(height = 2, width = 30)
		self.btnOnline.config(height = 2, width = 30)
		self.btnAcquire.pack()
		self.btnPreprocess.pack()
		self.btnOnline.pack()
		self.frame.pack()


	def btnAcquirePushed(self):	# CALLS TO ACQUISITION WINDOW
		
		acquire = AcquireWindow(self.master)
		self.master.mainloop()


	def btnPreprocessPushed(self):	# ASKS FOR THE DATA TO BE PROCESSED AND CALLS TO THE PIPELINE FUNCTIONS
		
		import global_variables
		import filter_files as filt
		import feature_extraction as feat
		import svm_classification as classif
		import plots

		import online_predict_test as onl_pred

		mainRoot = tk.Tk()
		mainRoot.withdraw()
		mainRoot.update()
		files_to_process = tkfiledialog.askopenfilenames(parent =mainRoot, initialdir = "./data",title = "Select file(s)",filetypes = (("txt files","*.txt"),("all files","*.*")))
		
		print("\nSelected Files: ", files_to_process, "\n")
		if files_to_process:
			global_variables.set_files_to_process(files_to_process)
			mainRoot.destroy()

# Processing
			trial_hor, trial_ver, trial_lab = filt.filter()
			
# Feature Extraction
			features = []
			features = feat.features(trial_hor, trial_ver)

# Classification
			classif.classification(features, trial_lab)

#	PLOTTING FUNCTIONS (FOR TESTING PURPOSES)

#			plots.feature3d_plot(features, trial_lab)
#			plots.feature2d_plot(features, trial_lab)
#			plots.trial_plot(trial_hor, trial_ver, trial_lab)
#			plots.derivative_signal(trial_hor, trial_ver, trial_lab)
#			plots.derivative_plots(trial_hor, trial_ver, trial_lab)
#			plots.feature_plot(features, trial_lab)
#			plots.movement_plot(trial_hor, trial_ver, trial_lab, "'Up'")
			
			saveRoot = tk.Tk()
			saveRoot.withdraw()
			saveRoot.update()
			save_wdw = SaveWindow(saveRoot)
			saveRoot.mainloop()
			


	def btnOnlinePushed(self):	# CALLS TO ONLINE PROCESSING PIPELINE

		import global_variables
		
		onlineRoot = tk.Tk()
		onlineRoot.model_name = tkfiledialog.askopenfilename(parent = onlineRoot, initialdir = "./models",title = "Select Model",filetypes = (("sav files","*.sav"),("all files","*.*")))
		
		if onlineRoot.model_name:

			global_variables.set_model(onlineRoot.model_name)
			online = OnlineClassification(onlineRoot)
		
		else:
			onlineRoot.destroy()



if __name__ == '__main__':

	global_variables.set_interface(True)
	root = tk.Tk()
	photo = tk.PhotoImage(file='./logos/Wheelchair_Logo.png')
	label = tk.Label(image=photo)
	label.image = photo
	label.pack()
	main = MainWindow(root)
	root.mainloop()