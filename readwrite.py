import io
import mmap
import os
import shutil
import concurrent.futures
from just import zxcvbn_result
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter


a = io.DEFAULT_BUFFER_SIZE

def lmao(inputfile):
	with open(inputfile, 'r', a*2) as fileIn, open(inputfile.replace('.txt','Results.txt'), 'w', a*3) as outputFile:
		tempheaders = "Password,Score,Guesses,CalcTime,OnlineRateLimited,OnlineNoRateLimited,OfflineFastHash,OfflineSlowhash\n"
		outputFile.write(tempheaders)
		num_lines = len(list(open(inputfile)))

		for indexRowNum, inputFileRow in enumerate(fileIn):
			if indexRowNum in range(0, num_lines):
				actualPass = str(inputFileRow.strip())
				lol = zxcvbn_result(actualPass)
				count4Last = 0
				lastElement = (len(lol) - 1)
				for item in lol:
					if(count4Last != lastElement):
						outputFile.write(str(item) + ',')
						#Also includes a final ',', has to be removed/discarded for further computations involving output files
						#Format of result: Pass,Score,Guesses,CalcTime, etc.
						count4Last += 1
					else:
						#Last element, we dont want a trailing ','
						outputFile.write((str(item)))
				outputFile.writelines('\n')

listToBeDone=[]
currdirectory = os.getcwd()
for file in os.listdir(currdirectory):
	#Find all the original policy text files, put them into the list
	#Can be *potentially* optimized
	if ("-zxcvbn" not in file) and ("Results-" not in file) and (file.endswith(".txt")):
		listToBeDone.append(file)

#argslist = ['1-Google-50k.txt', '5-Reddit-50k.txt']#Testing list...

'''if __name__ == "__main__":
	t = perf_counter()
	with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
		#88.43 seconds for 1 file
		#https://stackoverflow.com/questions/2562757/is-there-a-multithreaded-map-function
		l = list(executor.map(lambda inputfiles: lmao(inputfiles), argslist))	
	
	print(f"Time took: {perf_counter() - t:.2f}s")'''


#https://stackoverflow.com/questions/5442910/how-to-use-multiprocessing-pool-map-with-multiple-arguments
#https://www.thepythoncode.com/article/using-threads-in-python
