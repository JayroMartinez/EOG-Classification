# HERE WE READ DATA FROM OFFLINE AND ONLINE FILES
# AUTHOR: Jayro Martinez Cervero

def read_file(file_name):
	"""
# FUNCTION:	 	read_file(file_name)
# INPUT: 		Name of the file to read
# OUTPUT: 		Vertical & Horizontal components of the signal. Also a list with
#				the label corresponding to each timepoint
# DESCRIPTION:	Reads the data from a .txt file and returns it
# AUTHOR: 		Jayro Martinez Cervero
	"""
# Open the file
	file = open(file_name, 'r')
	values = file.readlines()
	
# Load data into new_values
	new_values = []
	labels_tmp = []
	hor_tmp = []
	ver_tmp = []

	for v in range(0,len(values)):
		new_values.insert(v, values[v].split(','))

# Load data from new_values into labels, horizontal & vertical
	for i in range(0,len(new_values)):
		
		labels_tmp.append(new_values[i][0])
		hor_tmp.append(new_values[i][2])
		ver_tmp.append(new_values[i][7])

# Remove '[' and cast into float
	for aux in range(0, len(labels_tmp)):
		if labels_tmp[aux].find("[") != -1:
			index = labels_tmp[aux].find("[")
			labels_tmp[aux] = labels_tmp[aux].replace(labels_tmp[aux][index], '')
			hor_tmp[aux] = float(hor_tmp[aux])
			ver_tmp[aux] = float(ver_tmp[aux])
		else:
			hor_tmp[aux] = float(hor_tmp[aux])
			ver_tmp[aux] = float(ver_tmp[aux])

	return hor_tmp, ver_tmp, labels_tmp



def read_online_file(file_name):
	"""
# FUNCTION:	 	read_file(file_name)
# INPUT: 		Name of the file to read
# OUTPUT: 		Vertical & Horizontal components of the signal. Also a list with
#				the label corresponding to each timepoint
# DESCRIPTION:	Reads the data from a .txt file and returns it
# AUTHOR: 		Jayro Martinez Cervero
	"""
# Open the file
	print(file_name)
	file = open(file_name, 'r')
	values = file.readlines()
	
# Load data into new_values
	new_values = []
	labels_tmp = []
	hor_tmp = []
	ver_tmp = []
	new_hor = []
	new_ver = []
	hor = []
	ver = []

	for v in range(0,len(values)):
		new_values.insert(v, values[v].split(']'))

# Load data from new_values into labels, horizontal & vertical
	for i in range(0,len(new_values)):
		hor_tmp.append(new_values[i][0])
		ver_tmp.append(new_values[i][1])

	for j in range(0, len(hor_tmp)):
		hor_tmp[j] = hor_tmp[j].replace(hor_tmp[j][0:2],'')
		ver_tmp[j] = ver_tmp[j].replace(ver_tmp[j][0:3],'')
		new_hor.insert(j, hor_tmp[j].split(','))
		new_ver.insert(j, ver_tmp[j].split(','))

		trial_hor = []
		trial_ver = []

		for k in range(0, len(new_hor[j])):
			trial_hor.append(float(new_hor[j][k]))
			trial_ver.append(float(new_ver[j][k]))

		hor.append(trial_hor)
		ver.append(trial_ver)

	return hor, ver