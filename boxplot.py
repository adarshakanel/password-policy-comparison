import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

fig = plt.figure(figsize =(50,50))

df = pd.read_csv(".\ResultsDirectory-v2\\1-Google-50kResults.csv", usecols=["Score", "Guesses"])
#print(df.Score)
#plt.boxplot([(df.Guesses)])
plt.boxplot([df.Score])


plt.show()
