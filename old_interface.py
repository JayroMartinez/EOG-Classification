import tkinter as tk
import tkinter.filedialog as tkfiledialog
import time
from datetime import datetime
import pickle
import sys
import os
from natsort import natsorted
import glob

#import connect_acquire_store as con
#import filter_files as filt
#import feature_extraction as feat
#import svm_classification as classif
#import online_classification as online
#import plots
#import global_variables

class MainWindow:
	def __init__(self, master):
	
		self.master = master
		master.title("EOG Wheelchair Project")
		master.geometry('600x400')
		self.btnAcquire = tk.Button(master, text='Acquire New Data', command = self.btnAcquirePushed)
		self.btnAcquire.grid(column=0, row=0)
		self.btnPreprocess = tk.Button(master, text='Process, Extract Features & Classify', command = self.btnPreprocessPushed)
		self.btnPreprocess.grid(column=0, row=1)
		self.btnOnline = tk.Button(master, text='Online Classification', command = self.btnOnlinePushed)
		self.btnOnline.grid(column=0, row=2)
		#master.mainloop()

	
	def btnSaveDataPushed(self, file_name):
	
		import global_variables
	
		new_file_name = "./data/"+file_name+".txt"
		global_variables.set_save_file(new_file_name)
		con.connect()


	def acquireNewFile(self):

		self.newFile_wdw = tk.Tk()
		self.newFile_wdw.title("Enter File Name")
		self.label = tk.Label(self.newFile_wdw, text="Enter File Name: ").grid(row=0)
		self.file_entry = tk.Entry(self.newFile_wdw)
		self.file_entry.grid(row=0,column=1)
		self.save_button = tk.Button(self.newFile_wdw, text="Acquire", command=lambda: self.btnSaveDataPushed(file_entry.get()))
		self.save_button.grid(row=1, column=0)
		self.newFile_wdw.mainloop()


	def acquireOldFile(self):

		import global_variables
	
		root = tk.Tk()
		root.withdraw()
		file_name = tkfiledialog.askopenfilename(parent =root, initialdir = "./data",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
	
		global_variables.set_save_file(file_name)
	
		con.connect()


	def btnAcquirePushed(self):
	
		self.acquireWindow = tk.Tk()
		self.acquireWindow.title("Acquire New Data")
		self.acquireWindow.geometry('600x400')
		self.btnNewData = tk.Button(acquireWindow, text='Create a New Data File or Overwrite Old Data File', command=self.acquireNewFile)
		self.btnNewData.grid(column=0, row=0)
		self.btnOldData = tk.Button(acquireWindow, text='Append to Old Data File', command=self.acquireOldFile)
		self.btnOldData.grid(column=0, row=1)
		self.acquireWindow.mainloop()


	def btnSaveModelPushed(model_name):

		import global_variables

		model_file_name = "./models/"+model_name+".sav"
		model = global_variables.get_model()
		pickle.dump(model, open(model_file_name, 'wb'))
	

	def btnPreprocessPushed(self):

		import global_variables
		import filter_files as filt
		import feature_extraction as feat
		import svm_classification as classif

		import os
	
		root = tk.Tk()
		root.withdraw()
		root.update()
		files_to_process = tkfiledialog.askopenfilenames(parent =root, initialdir = "./data",title = "Select file(s)",filetypes = (("txt files","*.txt"),("all files","*.*")))
		global_variables.set_files_to_process(files_to_process)
		root.destroy()

		# Processing
		trial_hor, trial_ver, trial_lab = filt.filter()

		# Feature Extraction
		features = []
		features = feat.features(trial_hor, trial_ver)

		# Classification
		classif.classification(features, trial_lab)

		save_wdw = tk.Tk()
		save_wdw.title("Enter File Name")
		label = tk.Label(save_wdw, text="Enter Model Name: ").grid(row=0)
		model_entry = tk.Entry(save_wdw)
		model_entry.grid(row=0,column=1)
		save_button = tk.Button(save_wdw, text="Save Model", command=lambda: btnSaveModelPushed(model_entry.get()))
		save_button.grid(row=1, column=0)
		save_wdw.mainloop()


	def btnOnlinePushed(self):
		print("Online")


if __name__ == '__main__':

	root = tk.Tk()
	mainWindow = MainWindow(root)
	root.mainloop()
	