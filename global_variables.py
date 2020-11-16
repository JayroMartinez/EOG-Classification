import random

##############################################################################
##																			
##                            GLOBAL VARIABLES                            
## 																		
##############################################################################

# LABELS TO USE IN THE SYSTEM
lab = ['Up', 'Down', 'Left', 'Right']

# NAME OF THE FILE WHERE TO SAVE ACQUIRED DATA
# We can use the same file for more than one block
save_file = None

# FILES TO LOAD, FILTER & CLASSIFY
files_to_process = []

# Sample Rate (250 Hz for Cyton Board)
sample_rate = 250
# Trial length (in seconds)
trial_lenght = 3
# Samples per trial
samples_per_trial = sample_rate * trial_lenght

# Online evaluation time (time between two evaluations of the signal to find actions) (in seconds))
evaluation_time = 0.5

# Create labels, random shuffle, insert 5 beeps at the beginning & append 'EXIT' at the end
samples_per_action = 5
# Set Label values
labels = lab * samples_per_action
random.shuffle(labels)

for i in range(0,5):
	labels.insert(0,"beep")
labels.append('EXIT')

# Create an iterator over label array
iter = 0
# Create a counter for the number of datapoints
cont = 0

# Filter lowcut frequency
lowcut = 0.05
# Filter highcut frequency
highcut = 20
# Filter order
order = 2


# Classification Model
model = []

# Interface
interface = False

# Online Acquisition Started
online_started = False

# Online Data file
online_data_file = []
online_aux_file = []


####################################################################
# FUNCTION:		get_global_variable()
# INPUT:		None
# OUTPUT:		Global Variable
# DESCRIPTION:	Returns the value of the particular Global Variable
####################################################################
def get_lab(): return lab


def get_save_file(): return save_file


def get_files_to_process(): return files_to_process


def get_sample_rate(): return sample_rate


def get_trial_lenght(): return trial_lenght


def get_samples_per_trial(): return samples_per_trial


def get_evaluation_time(): return evaluation_time


def get_samples_per_action(): return samples_per_action


def get_labels(): return labels


def get_iter(): return iter


def get_cont(): return cont


def get_lowcut(): return lowcut


def get_highcut(): return highcut


def get_order(): return order


def get_model(): return model


def get_interface(): return interface


def get_online_started(): return online_started


def get_online_data_file(): return online_data_file


def get_online_aux_file(): return online_aux_file


####################################################################
# FUNCTION:		set_global_variable()
# INPUT:		Value of the variable to set
# OUTPUT:		None
# DESCRIPTION:	Sets the Global Variable values
####################################################################
def set_model(mod): 
	global model

	model = mod


def set_save_file(filename): 
	global save_file 

	save_file = filename


def set_files_to_process(files): 
	global files_to_process

	files_to_process = files


def set_cont(con): 
	global cont

	cont = con


def set_iter(it): 
	global iter

	iter = it


def set_interface(inter):
	global interface

	interface = inter


def set_online_started(online):
	global online_started

	online_started = online


def set_online_data_file(filename):
	global online_data_file

	online_data_file = filename


def set_online_aux_file(filename):
	global online_aux_file

	online_aux_file = filename


####################################################################
# FUNCTION:		reset_global_variable()
# INPUT:		None
# OUTPUT:		None
# DESCRIPTION:	Resets the Global Variable values
####################################################################
def reset_labels():
	global labels, samples_per_action, lab

	labels = lab * samples_per_action
	random.shuffle(labels)

	for i in range(0,5):
		labels.insert(0,"beep")
	labels.append('EXIT')



####################################################################
# FUNCTIONS AND VARIABLES FOR FAKE ONLINE DATA (FOR TESTING PURPOSES)
####################################################################
predicted_times = []
predicted_labels = []

def get_predicted_times(): return predicted_times


def get_predicted_labels(): return predicted_labels


def append_predicted_times(pred_tm):
	global predicted_times

	predicted_times.append(pred_tm)


def append_predicted_labels(pred_lb):
	global predicted_labels

	predicted_labels.append(pred_lb)