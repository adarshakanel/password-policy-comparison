import pandas as pd
import matplotlib.pyplot as plt
import os

filetxtList = []
for file in os.listdir(os.getcwd()):
	#Find all the result text files, put them into the list
	#Can be *potentially* optimized
	if ("Results" in file) and (file.endswith(".csv")):
		filetxtList.append(file)

names1=['Password','Score','Guesses','CalcTime','OnlineRL','OnlineNoRL','OfflineFH','OfflineSH']
a = 'temp02.csv'
dataset = pd.read_csv(a, 
		usecols=['Password','Score'], header=None)

print(dataset.head())