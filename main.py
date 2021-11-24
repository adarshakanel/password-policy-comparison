import os
from os import path
import shutil
from zxcvbn import zxcvbn

#initialize empty lists for original and result files
filesToBeDone = []
resultFiles = []

currdirectory = os.getcwd()
for file in os.listdir(currdirectory):
	if file.endswith(".txt"):
		filesToBeDone.append(file)

print("Old files list: ")
print(filesToBeDone)
#Above supposed to contain OG pass policy files

for eachOldFile in filesToBeDone:
	a = 'Results'+ eachOldFile
	resultFiles.append(a)

print("New files(results) list:" )
print(resultFiles)
print('\n')

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
	except:
		return print("Error\n")

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

#resultDirectory = "Results1"
if not os.path.exists('ResultsDirectory'):
	os.mkdir('ResultsDirectory')
files = os.listdir(currdirectory)
destination1=currdirectory+"\ResultsDirectory"
results=[]
for f in files:
    if (f.startswith("Results")):
    	results.append(f)
    	shutil.move(f, destination1)
#Move results files to one directory

					

		

#References:
#Primary source --> https://github.com/dwolfhub/zxcvbn-python
#Another one --> https://github.com/dropbox/zxcvbn
#https://stackoverflow.com/questions/21414639/convert-timedelta-to-floating-point
#https://stackoverflow.com/questions/3845362/how-can-i-check-if-a-key-exists-in-a-dictionary