import pandas as pd
import os
from time import perf_counter
import csv
from concurrent.futures import ThreadPoolExecutor

#This works, just extra empty row b/w every entry:
# i.e. pass1 score1 guess1 ...
#  emptyrow
# 	   pass2 score2 guess2 ..
# emptyrow so on
#fixed: https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row

filetxtList = []
for file in os.listdir(os.getcwd()):
	#Find all the result text files, put them into the list
	#Can be *potentially* optimized
	if ("Results" in file) and (file.endswith(".txt")):
		filetxtList.append(file)

print(filetxtList)
limit = len(filetxtList)
print("Number of results txt files to be converted: ", limit)

t = perf_counter()

def try_convert(inputtextfile):
	with open(inputtextfile, 'r') as csvfile:
			csvfile1 = csv.reader(csvfile, delimiter=',')
			with  open(inputtextfile.replace('.txt','.csv'), 'w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter=',')
				for row in csvfile1:
					writer.writerow(row)

			print(f"Time took for converting this file: {perf_counter() - t:.2f}s")

if __name__ == "__main__":
	t = perf_counter()
	with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
		#https://stackoverflow.com/questions/2562757/is-there-a-multithreaded-map-function
		l = list(executor.map(lambda inputfiles: try_convert(inputfiles), filetxtList))


#https://stackoverflow.com/questions/50101543/converting-txt-to-csv-python
