####################################################################
####################################################################

## PROBABLEMENTE FUNCION INUTIL

####################################################################
####################################################################

from openbci import cyton as board
import time


def connect():

# CONNECTION PARAMETERS
	port = '/dev/tty.usbserial-DM01HL5T'
	baud = 115200
	filter_data = False
	scaled_output = True
	daisy = False
	aux = False
	impedance = False
	log = False
	timeout = None

# CONNECTION ESTABLISHMENT
	connection = board.OpenBCICyton(port=port,
									baud=baud,
									filter_data=filter_data,
									scaled_output=scaled_output,
									daisy=daisy,
									aux=aux,
									impedance=impedance,
									log=log,
									timeout=timeout)

# CONFIGURATION
	time.sleep(1)
	# Turn Off channels [1, 3, 4, 5, 6, 8]
	connection.ser.write(b'1')
	connection.ser.write(b'3')
	connection.ser.write(b'4')
	connection.ser.write(b'5')
	connection.ser.write(b'6')
	connection.ser.write(b'8')
	# For channels 2 & 7: 
	# Power 'On'
	# Gain set to 'x8'
	# Input type to 'normal'
	# 'Remove' channel from bias
	# 'disconnect' channel from SRB2
	# 'disconnect' all channels from SRB1
	connection.ser.write(b'x2040000X')
	connection.ser.write(b'x7040000X')

	return connection

if __name__ == '__main__':
	connect()
