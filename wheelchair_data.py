####################################################################
####################################################################

## PROBABLEMENTE FUNCION INUTIL

####################################################################
####################################################################
from pydub import AudioSegment
from pydub.playback import play
import random


def handle_streamed_data(sample):
	
	tmp_lab = labels[iter]

	if cont == 0:
		if tmp_lab == 'EXIT':
			file.close()
			wh.connection.stop()
			wh.connection.disconnect()
			print("**********************************")
			print("**********************************")
			print("**   TRAINNING BLOCK FINISHED   **")
			print("**********************************")
			print("**********************************")
			time.sleep(1)
			exit()
			#exit = True
		else:
			song_name = "./audio/"+tmp_lab+".mp3"
			song = AudioSegment.from_mp3(song_name)
			play(song)
			cont += 1
			sample.channel_data.insert(0,tmp_lab)
			str_chn_dta =  ' '.join([str(sample.channel_data)])
			file.write(str_chn_dta)
			file.write('\n')

	elif cont < 749:
		cont += 1
		sample.channel_data.insert(0,tmp_lab)
		str_chn_dta =  ' '.join([str(sample.channel_data)])
		file.write(str_chn_dta)
		file.write('\n')
	else:
		cont = 0
		iter +=1
		sample.channel_data.insert(0,tmp_lab)
		str_chn_dta =  ' '.join([str(sample.channel_data)])
		file.write(str_chn_dta)
		file.write('\n')

def acquire_store():
	connection.print_register_settings()  
	connection.start_streaming(handle_streamed_data)
	connection.loop()

if __name__ == '__main__':

# Create labels, random shuffle & insert 5 beeps at the beginning
	lab = ['Up', 'Down', 'Left', 'Right', 'Blink', 'Double_Blink', 'Close_Eyes']
	labels = lab*10
	random.shuffle(labels)
	for i in range(0,5):
		labels.insert(0,"beep")
	labels.append('EXIT')
# Define and open file name were we are going to save the data
	filename = "File_1.txt"
	file = open(filename, 'w')
# Create an iterator over label array
	iter = 0
# Create a counter for the number of datapoints (250 per second, 750 per trial)
	cont = 0
# Call to acquire & store function
	acquire_store()