# importing pandas library
import pandas as pd
import time
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

'''filename = '8-YahooResults.txt'

data1 = pd.read_csv(filename, header = None)

data1.to_csv('YahooCSV1.csv', index = None, header = False)
#header = false --> no more column indexs above every column....

df = pd.read_csv('YahooCSV1.csv')
'''


filetxtList = []
for file in os.listdir(os.getcwd()):
	#Find all the result text files in the cwd (which is the results subfolder from the root!), put them into the list
	if ("Results" in file) and (file.endswith(".txt")):
		#Naming convention and dont add bloat
		filetxtList.append(file)

print(filetxtList)

limit = len(filetxtList)
print("Number of results txt files to be converted: ", limit)

t = time.process_time()

resultcsvlist = []

'''
def txt2csv(inputtextf):
	b = inputtextf.replace('.txt','000001.csv')
	#Results1.txt --> Results1.csv...
	tempdata = pd.read_csv(inputtextf, header = None)
	tempdata.to_csv(b, index = None, header = False)

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
	l = list(executor.map(lambda inputfiles: txt2csv(inputfiles), filetxtList))	
	#Total time taken for 9 files ~ 4.34375s
'''


for eachTXT in filetxtList:
	tempoutcsv = eachTXT.replace('.txt','.csv')
	tempdata1 = pd.read_csv(eachTXT, header = None)
	tempdata1.to_csv(tempoutcsv, index = None, header = False)

#	total time taken for 9 files ~  3.875s


elapsed_time = time.process_time() - t

print("Total operation time: {}".format(elapsed_time))
'''
References:
1) https://stackoverflow.com/questions/49608656/saving-a-dataframe-to-csv-file-python
2) https://stackoverflow.com/questions/56166681/how-to-write-a-pandas-dataframe-to-csv-file-with-custom-header
'''