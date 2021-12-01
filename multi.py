import os
import shutil
import traceback
import sys
import glob
import time
import threading
from queue import Queue
from zxcvbnagent import zxcvbn_result
from time import perf_counter
from readwrite import lmao
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

start_time = time.monotonic()

root = os.getcwd()	#type: String

#initialize empty lists for original and result files
filesToBeDone = []
resultFiles = []

try:
	folderName = input("Enter folder name that contains the UNprocessed text files.\nCARE CAPITALIZATION AND SPELLING!\nLeave blank or put 0 if files are in the current directory: ")
	resultfolderName = input("Enter name of the folder that will contain the results: ")
except:
	#Trying to accept blank inputs, idk how otherwise, welcome 4 ideas
	folderName = None

if (folderName is None) or (len(folderName)==0) or (len(folderName) == 1) :
	print("Checking the current working directory.")
	temp1 = root
	if not glob.glob("*.txt"):
	#anotha way: if len(glob.glob("*.txt")) == 0:
	#No .txt files found in cwd, exit program
		sys.exit('No text files found in the cwd. Exiting program.')

	for file in os.listdir(temp1):
	#Find all the original policy text files, put them into the list
	#Can be *potentially* optimized (actually nvm: https://www.peterbe.com/plog/fastest-filename-extension-in-python)
		if ("-zxcvbn" not in file) and ("Results" not in file) and (file.endswith(".txt")):
			filesToBeDone.append(file)
else:
	#Create new string variable that contains root file path (from os.getcwd()) and joins '/'
	temp1 = root + '/' + folderName

if (resultfolderName is None) or (len(resultfolderName) == 0) or (len(resultfolderName) == 1):
	tempdest2 = root + '/' + resultfolderName
	if not os.path.exists(tempdest2):
	#Creates new folder for storing results and cleaning up the working folder
		os.mkdir('ResultsDirectory-temp')
		

else:
	tempdest2 = root+"\ResultsDirectory-temp"
	if not os.path.exists(tempdest2):
	#Creates new folder for storing results and cleaning up the working folder
		os.mkdir(resultfolderName)


if(temp1!=root):
	if (os.path.exists(temp1)):
		print("Folder exists. Traversing it.")
		os.chdir(temp1)
		#Change working directory to sub-folder 
		if not glob.glob("*.txt"):
			#anotha way: if len(glob.glob("*.txt")) == 0:
			#No .txt files found in cwd, exit program
			sys.exit('No text files found in the cwd. Exiting...')
		else:
			for filename in os.listdir(temp1):
			#Find all the original policy text files, put them into the list
			#Can be *potentially* optimized
				if (("-zxcvbn" not in filename) and ("Results" not in filename) and (filename.endswith(".txt"))):
					#Ensure proper naming is followed to avoid including unneccessary files...
					print("File: " + str(filename) + " found! Adding to list and moving to 'working' folder!")
					filesToBeDone.append(filename)
					filename = os.path.join(temp1, filename)
					destination = root
					shutil.copy2(filename, destination)
	else:
		sys.exit("Folder not found, run this file again and double-check the name of the folder!")



#https://www.peterbe.com/plog/fastest-filename-extension-in-python
#https://stackoverflow.com/questions/51528103/python-copying-specific-files-from-a-list-into-a-new-folder

os.chdir(root)

print("List of files that will be processed: ")
print(filesToBeDone)

for eachOldFile in filesToBeDone:
	#Create new files for storing results after running zxcvbn tests on policy files
	#Example: "Policy1.txt" --> "Results-Policy1.txt"
	a = 'Results-'+ eachOldFile
	resultFiles.append(a)
	#Do this for all old files and store the resultant files in the resultFiles list.

print("List of files containing the result(s):" )
print(resultFiles)

limit = len(filesToBeDone)
print("Number of eligible files in current directory to be processed: " + str(limit))

#just4Yahoo = ['4-Yahoo-50K.txt']#Just for no.8

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
	l = list(executor.map(lambda inputfiles: lmao(inputfiles), filesToBeDone))	
	print("Writing to file complete. If available, moving on to next file.")
		
print('Total operation time in seconds: ', time.monotonic() - start_time)

#Now, to clean up everything, move resultant files to a new folder (created if doesn't already exist)
#resultDirectory = "Results1"

files = os.listdir(root)
#destination1=root+"\ResultsDirectory-v0"
destination1 = tempdest2
for f in files:
	#Check cwd which is where the processed resultant files are stored
	#temporarily...
	if ("Results" in f):
		shutil.move(f, destination1)
	if f.startswith("properconverter"):
		shutil.copy2(f, destination1)

print("Moving files to results directory complete. Starting conversion to csv...\n")
os.chdir(destination1)
exec(open('properconverter.py').read())
print("Operation finished.")
print('Total operation time in seconds: ', time.monotonic() - start_time)

#All done!		

#References:
#Primary source --> https://github.com/dwolfhub/zxcvbn-python
#Another one --> https://github.com/dropbox/zxcvbn
#https://stackoverflow.com/questions/21414639/convert-timedelta-to-floating-point
#https://stackoverflow.com/questions/3845362/how-can-i-check-if-a-key-exists-in-a-dictionary
#https://linuxhandbook.com/python-write-list-file/
#https://pythonguides.com/python-write-a-list-to-csv/
#https://codefather.tech/blog/write-list-to-a-file-in-python/
#https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python?page=2&tab=Votes
#https://www.w3schools.com/python/python_for_loops.asp
#https://stackabuse.com/python-get-number-of-elements-in-a-list/
#https://linuxize.com/post/python-get-change-current-working-directory/#:~:text=To%20find%20the%20current%20working,chdir(path)%20.
#https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
#https://stackoverflow.com/questions/3702675/how-to-catch-and-print-the-full-exception-traceback-without-halting-exiting-the
#https://stackoverflow.com/questions/62255438/deleting-files-of-specific-extension-using-in-python
#https://stackoverflow.com/questions/7370801/how-to-measure-elapsed-time-in-python
#https://stackoverflow.com/questions/61843030/how-to-use-one-python-script-to-run-another-python-script-and-pass-variables-to
#https://stackoverflow.com/questions/50101543/converting-txt-to-csv-python
#Threading:
#https://thispointer.com/python-how-to-create-a-thread-to-run-a-function-in-parallel/
#https://www.thepythoncode.com/article/using-threads-in-python
