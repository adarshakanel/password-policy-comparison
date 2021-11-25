import os
from os import path
import shutil
from zxcvbn import zxcvbn
import traceback
import sys
import glob

#initialize empty lists for original and result files
filesToBeDone = []
resultFiles = []

currdirectory = os.getcwd()
print("Current working directory: " + currdirectory)

if not glob.glob("*.txt"):
	#anotha way: if len(glob.glob("*.txt")) == 0:
  sys.exit('No text files found in the cwd. Exiting...')

for file in os.listdir(currdirectory):
	#Find all the original policy text files, put them into the list
	#Can be *potentially* optimized
	if file.endswith(".txt"):
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
print("Number of files in current directory to be processed: " + str(limit))

def zxcvbn_result(lineInput):
	#:param - input password, which is passed as a string
	#:return - list containing results from performing 'zxcvbn' on input
	try:
		resultsRow = []
		#Empty list initialized for storing the output 
		results = zxcvbn(lineInput)
		#sequence = results["sequence"]
		tempPass = results['password']
		#The input password (obtained by extracting line by line from the policy text files)
		tempScore = results['score']
		#Integer from 0-4, 0 being too guessable, 4 being very unguessable
		tempCalcTime = results['calc_time']
		tempCalcTime = tempCalcTime.total_seconds()
		#how long it took zxcvbn to calculate an answer, in milliseconds. Since tempCalcTime is originally a 
		# datetime.TimeDelta type, converted to number of seconds contained in the duration using total_seconds()
		tempGuesses = results['guesses']
		#estimated guesses needed to crack password

		#Following are estimations of different scenarios to 'crack' the password
		tempOnlineRL = results['crack_times_seconds']['online_throttling_100_per_hour']
		# online attack on a service that ratelimits password auth attempts.
		tempOnlineNoRL = results['crack_times_seconds']['online_no_throttling_10_per_second']
		#  online attack on a service that doesn't ratelimit, or where an attacker has outsmarted ratelimiting.
		tempOfflineFH = results['crack_times_seconds']['offline_fast_hashing_1e10_per_second']
		#offline attack with user-unique salting but a fast hash function like SHA-1, SHA-256 or MD5
		tempOfflineSH = results['crack_times_seconds']['offline_slow_hashing_1e4_per_second']
		## offline attack. assumes multiple attackers, proper user-unique salting, and a slow hash function w/ moderate work factor, such as bcrypt, scrypt, PBKDF2.

		resultsRow = [(tempPass), (tempScore), (tempGuesses), (tempCalcTime), 
						(tempOnlineRL), (tempOnlineNoRL), (tempOfflineFH), (tempOfflineSH)]
		return resultsRow

	except Exception: 
		#Yeah idk about this part but oh well, should be helpful still
		print("Error:\n")
		print(traceback.format_exc())
		traceback.print_exc()

for i in range(0, limit):
	#A bit inefficient way in which all the OG .txt files are read and the results files are produced 

	with open(filesToBeDone[i], 'r') as inputFile, open(resultFiles[i], 'w') as outputFile:

			num_lines = len(list(open(filesToBeDone[i])))
			print("Opening file: " + filesToBeDone[i])
			print("Number of passwords in file: " + str(num_lines) +"\n")
			print("Writing results to file: " + resultFiles[i])
			tempheaders = "Password,Score,Guesses,CalcTime,OnlineRateLimited,OnlineNoRateLimited,OfflineFastHash,OfflineSlowhash\n"
			outputFile.write(tempheaders)
			print("\n")

			for indexRowNum, inputFileRow in enumerate(inputFile):
				
				if indexRowNum in range(0, num_lines):
					actualPass = str(inputFileRow.strip())
					lol = zxcvbn_result(actualPass)
					for item in lol:
						outputFile.write(str(item) + ',')
						#Also includes a final ',', has to be removed/discarded for further computations involving output files
						#Format of result: Pass,Score,Guesses,CalcTime, etc.
					outputFile.writelines('\n')
					#Continue

			print("Writing to file complete. If available, moving on to next file.")

#Now, to clean up everything, move resultant files to a new folder (created if doesn't already exist)
#resultDirectory = "Results1"

if not os.path.exists('ResultsDirectory'):
	#Self-explanatory
	os.mkdir('ResultsDirectory')

files = os.listdir(currdirectory)
destination1=currdirectory+"\ResultsDirectory"
for f in files:
    if (f.startswith("Results-")):
    	shutil.move(f, destination1)
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
