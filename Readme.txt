Peltier Cooler Project

Main Programs:
*FLoop: 
	-Arduino program. Found within the "Arduino Programs" directory. 
	-Controls the Peltier's, monitors temperature, and communicates with the python script.
	-Loaded onto Arduino. Does not have to be uploaded every use.

	
*Com.py: 
	-Python Script. Found within the "Python Scripts" directory
	-Reads the temperature outputs from the Arduino, logs them in files, and emails if there is failure
	-Must be ran every use


How to run Com.py(NOTE: CURRENTLY ON WORKS ON WINDOWS):
  Requirements-
	*python:
	  There are many options to install python. There are tutorials for Windows if googled, or you could download Enthought Canopy.
	*pip:
	  Download http://www.pip-installer.org/en/latest/installing.html
	  In cmd, cd to the directory of the file downloaded and type: python get-pip.py
	*pyserial:
	  After pip is installed, type in cmd: python -m pip install pyserial
	*pyqtgraph
	  After pip is installed, type in cmd: python -m pip install pyqtgraph
  Procedure 1 (command line)-
	1. cd to the directory of the python script. Ex: cd C:\Users\Your_Username\Documents\Github\Peltier-Cooler\PythonScripts
	2. type: python -B Com.py
	3. Enter the com port. Ex: Usually type: 0 
	4. Enter how often you want data output

  Procedure 2 (user interface)-
	1. go to the Pelter-Cooler folder
	2. double click: RunPython
	3. Enter the com port. Ex: Usually type: 0 
	4. Enter how often you want data output

How to run FLoop:
  Requirements-
	*Arduino IDE:
	  https://www.arduino.cc/en/Main/Software
  Procedure-
	1. The Arduino program is likely already on the board. It automatically starts running when the Arduino is turned on.
	2. If not loaded on, run the Arduino IDE and open FLoop
	3. Click the upload button on the top left

Where to find data outputs: 
	- The data outputs are in a folder called "Logs" inside the PythonScripts directory
	- They are in the form of csv files and include a timestamp in their names. 
	
*NOTE: There are heavily commented versions of the programs left in the folders
*These may be used for better understanding of the programs
*However, they are likely obsolete and should not be run
*The other files/programs are either irrelevant or tests
