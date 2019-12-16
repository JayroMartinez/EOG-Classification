####################################################################
####################################################################

## PROBABLEMENTE FUNCION INUTIL

####################################################################
####################################################################
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

if __name__ == '__main__':

	file = open("Jayro_5.txt", 'r')
	values = file.readlines()
	#print values
	new_values = []
	for v in range(0,len(values)):
		new_values.insert(v, values[v].split(','))

	x = range(1,len(new_values)-1)
	
	labels = []
	hor = []
	ver = []
	
	for i in range(1,len(new_values)-1):
		labels.append(new_values[i][0])
		hor.append(new_values[i][2])
		ver.append(new_values[i][7])

	for aux in range(0, len(labels)):
		if labels[aux].find("[") != -1:
			index = labels[aux].find("[")
			labels[aux] = labels[aux].replace(labels[aux][index], '')
			hor[aux] =float(hor[aux])
			ver[aux] =float(ver[aux])
		else:
			hor[aux] =float(hor[aux])
			ver[aux] =float(ver[aux])

	#print(a)

	step_hor = (max(hor) - min(hor))/10
	step_ver = (max(hor) - min(hor))/10

#	plt.subplot(311)
#	plt.plot(x, hor)
#	plt.title("Horizontal")
#	plt.xticks(np.arange(0,len(x),step=750))
#	plt.yticks(np.arange(min(hor), max(hor), step=step_hor))
#	#plt.show()

#	plt.subplot(312)
#	plt.plot(x, ver)
#	plt.title("Vertical")
#	plt.xticks(np.arange(0,len(x),step=750))
#	plt.yticks(np.arange(min(ver), max(ver), step=step_ver))
#	#plt.show()

#	plt.subplot(313)
#	plt.plot(x, hor, label = 'Horizontal')
#	plt.plot(x, ver, label = 'Vertical')
#	plt.title("Both")
#	plt.legend()
#	plt.xticks(np.arange(0,len(x),step=750))
#	#plt.yticks(np.arange(min(ver), max(ver), step=step_ver))
#	plt.show()

	colors = []
	for i in range(0,len(labels)-1):
		if labels[i] == "'Up'":
			colors.append('k')
		elif labels[i] == "'Down'":
			colors.append('tab:green')
		elif labels[i] == "'Left'":
			colors.append('tab:orange')
		elif labels[i] == "'Right'":
			colors.append('tab:red')
		elif labels[i] == "'Blink'":
			colors.append('tab:blue')
		elif labels[i] == "'Double_Blink'":
			colors.append('tab:pink')
		elif labels[i] == "'Close_Eyes'":
			colors.append('tab:brown')
		else:
			colors.append('tab:gray')

	lines_ver = [((x0,ver0), (x1,ver1)) for x0, ver0, x1, ver1 in zip(x[:-1], ver[:-1], x[1:], ver[1:])]
	lines_hor = [((x0,hor0), (x1,hor1)) for x0, hor0, x1, hor1 in zip(x[:-1], hor[:-1], x[1:], hor[1:])]
	#colored_lines = LineCollection(lines, colors=colors, linewidths=(2,))
	colored_lines_ver = LineCollection(lines_ver, colors=colors, linewidths=(2,), linestyle = '-', label='Vertical')
	colored_lines_hor = LineCollection(lines_hor, colors=colors, linewidths=(1,), linestyle = ':', label='Horizontal')

	fig, ax = plt.subplots(1)
	#ax.set_xticks(np.arange(0,len(x),step=750))
	ax.add_collection(colored_lines_ver)
	ax.add_collection(colored_lines_hor)
	ax.autoscale_view()
	ax.legend()
	for j in range(0,len(x)-1, 750):
		plt.axvline(x=j, color='tab:gray', linestyle=':')
	#ax.set_facecolor('tab:gray')
	plt.show()

	file.close()