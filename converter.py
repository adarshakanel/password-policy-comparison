import pandas as pd
import os
from time import perf_counter
import csv

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

for i in range(0, limit):
	with open(filetxtList[i], 'r') as csvfile:
			csvfile1 = csv.reader(csvfile, delimiter=',')
			with  open(filetxtList[i].replace('.txt','.csv'), 'w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter=',')
				for row in csvfile1:
					writer.writerow(row)

			print(f"Time took for converting this file: {perf_counter() - t:.2f}s")

print(f"Final operation time: {perf_counter() - t:.2f}s")


#https://stackoverflow.com/questions/50101543/converting-txt-to-csv-python