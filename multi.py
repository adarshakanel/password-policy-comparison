import os
import shutil
import traceback
import sys
import glob
import time
import threading
from queue import Queue
from just import zxcvbn_result
from time import perf_counter
from readwrite import lmao
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

start_time = time.monotonic()

#initialize empty lists for original and result files
filesToBeDone = []
resultFiles = []

currdirectory = os.getcwd()
print("Current working directory: " + currdirectory)

if not glob.glob("*.txt"):
	#anotha way: if len(glob.glob("*.txt")) == 0:
	#No .txt files found in cwd, exit program
  sys.exit('No text files found in the cwd. Exiting...')

for file in os.listdir(currdirectory):
	#Find all the original policy text files, put them into the list
	#Can be *potentially* optimized
	if ("-zxcvbn" not in file) and ("Results" not in file) and (file.endswith(".txt")):
		filesToBeDone.append(file)

'''
if os.path.exists('FilesDirectory'):
	new = currdirectory + '\FilesDirectory'
	os.chdir(new)
	#"move" to inner directory 
	for file in os.listdir(os.getcwd()):
		filesToBeDone.append(file)
os.chdir(currdirectory)
'''
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

tempTry = filesToBeDone[0:2]

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
	l = list(executor.map(lambda inputfiles: lmao(inputfiles), filesToBeDone))	
	print("Writing to file complete. If available, moving on to next file.")
		
print('Total operation time in seconds: ', time.monotonic() - start_time)

#Now, to clean up everything, move resultant files to a new folder (created if doesn't already exist)
#resultDirectory = "Results1"

if not os.path.exists('ResultsDirectory-v2'):
	#Self-explanatory
	os.mkdir('ResultsDirectory-v2')

files = os.listdir(currdirectory)
destination1=currdirectory+"\ResultsDirectory-v2"
for f in files:
    if (("Results" in f) or (f.startswith("converter"))):
    	shutil.move(f, destination1)

print("Moving files to results directory complete. Starting conversion to csv...\n")
os.chdir(destination1)
exec(open('converter.py').read())
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