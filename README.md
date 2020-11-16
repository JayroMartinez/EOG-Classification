# EOG-Classification
This project is an EOG signal classificator. The aim of the project was to create a system that could be easily connected to a communication or movement assistance device like a wheelchair, any kind of speller application, or merely a computer mouse and a virtual keyboard, using open (or almost open) technologies.

The code is created to acquire the data using [OpenBCI Cyton biosignal acquisition board](https://docs.openbci.com/docs/02Cyton/CytonLanding "OpenBCI Cyton documentation"). The processing has been done with Raspberri Pi and MacOS.

The code uses [OpenBCI Python driver](https://github.com/openbci-archive/OpenBCI_Python "OpenBCI Python repository on GitHub"), nowadays deprecated, to communicate with the board and acquire the signals. To correctly run this third party code, some work is needed. It should be mentioned that the OpenBCI Python driver code that is in this repository has some minimal changes in order to fit our interests.

THE PROJECT IS DISCONTINUED. Of course you can use it, modify it and do whatever you want with it. In case you need help don't hesitate to contact me but, because this was done some time ago, I do not promise to be able to help.

A deeper explanaition on the project concerning this code, take a look to the reference paper:
[Martínez-Cerveró, J.; Ardali, M.K.; Jaramillo-Gonzalez, A.; Wu, S.; Tonin, A.; Birbaumer, N.; Chaudhary, U. Open Software/Hardware Platform for Human-Computer Interface Based on Electrooculography (EOG) Signal Classification. Sensors 2020, 20, 2443.](https://www.mdpi.com/1424-8220/20/9/2443#cite "Open Software/Hardware Platform for Human-Computer Interface Based on Electrooculography (EOG) Signal Classification").

To run the system, execute *interface.py*. I know the code is tremendously messy and probably not written with the best practices. Aplologies for this, is my first approach to Python.
