import os
from zxcvbn import zxcvbn

filesToBeDone = []
filesDone = []
resultFiles = []

currdirectory = os.getcwd()
for file in os.listdir(currdirectory):
	if file.endswith(".txt"):
		filesToBeDone.append(file)

print("Old files list: ")
print(filesToBeDone)

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
		results = zxcvbn(lineInput)
		#sequence = results["sequence"]
		tempPass = results['password']
		tempScore = results['score']
		tempCalcTime = results['calc_time']
		tempGuesses = results['guesses']

		resultsRow = [str(tempPass), str(tempScore), str(tempGuesses), str(tempCalcTime)]
		return resultsRow
	except:
		return print("Error\n")

for i in range(0, 8):
	#ik this is cringe but wateva

	with open(filesToBeDone[i], 'r') as inputFile, open(resultFiles[i], 'w') as outputFile:

			num_lines = len(list(open(filesToBeDone[i])))
			print("Opening file: " + filesToBeDone[i])
			print("Number of passwords in file: " + str(num_lines) +"\n")
			print("Writing results to file: " + resultFiles[i])
			tempheaders = "Password Score Guesses CalcTime\n"
			outputFile.write(tempheaders)
			print("\n")

			for indexRowNum, inputFileRow in enumerate(inputFile):
				
				if indexRowNum in range(0, 4):
					actualPass = str(inputFileRow.strip())
					#print(intoMachine)
					lol = zxcvbn_result(actualPass)
					for item in lol:
						outputFile.write(item + ' ')
					outputFile.writelines('\n')

			print("Writing to file complete. If available, moving on to next file.")
					

		