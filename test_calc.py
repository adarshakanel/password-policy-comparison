import os
from os import path
from re import I, split
import shutil
from zxcvbn import zxcvbn
import traceback
import sys
import glob
import math


# initialize empty lists for original and result files
filesToBeDone = []
resultFiles = "File_data.txt"

currdirectory = os.getcwd()+"\ResultsDirectory-v2"

print("Current working directory: " + currdirectory)

if not glob.glob("*.txt"):
    # anotha way: if len(glob.glob("*.txt")) == 0:
    sys.exit('No text files found in the cwd. Exiting...')

for file in os.listdir(currdirectory):
    # Find all the original policy text files, put them into the list
    # Can be *potentially* optimized
    if ("-zxcvbn" not in file) and (file.endswith("Results.txt")):
        filesToBeDone.append(file)


def findAverage(numerator, index):
    return numerator / index


def findStd(stdArray, fileSize, average):
    # print(stdArray)
    numerator = 0
    for element in stdArray:
        summation = element - average
        numerator += summation**2
    frac = numerator / fileSize
    return math.sqrt(frac)


def findValue():
    with open(resultFiles, 'w') as result:
        result.writelines(
            "file_name, average_guess, average_guess_log_10, std_guess, average_score, std_score, average_guess_time, guess_time_std")
        for file in filesToBeDone:
            stdScoreArray = []
            stdGuessArray = []
            stdGuessTimeArray = []
            with open("ResultsDirectory-v2/" + file, 'r') as inputFile:
                for index, line in enumerate(inputFile):
                    if index == 0:
                        continue
                    splitString = line.split(",")
                    stdScoreArray.append(float(splitString[1]))
                    stdGuessArray.append(float(splitString[2]))
                    stdGuessTimeArray.append(float(splitString[3]))
                fileLength = len(
                    open("ResultsDirectory-v2/" + file, 'r').readlines())
                score = sum(stdScoreArray)
                guess = sum(stdGuessArray)
                guessTime = sum(stdGuessTimeArray)
                averageGuess = findAverage(guess, fileLength)
                averageScore = findAverage(score, fileLength)
                averageGuessTime = findAverage(guessTime, fileLength)
                stdScore = findStd(stdScoreArray, fileLength, averageScore)
                stdGuess = findStd(stdGuessArray, fileLength, averageGuess)
                stdGuessTime = findStd(
                    stdGuessTimeArray, fileLength, averageGuess)
                fileData = [averageGuess, math.log(averageGuess, 10),
                            stdGuess, averageScore, stdScore, averageGuessTime, stdGuessTime]
                data = [inputFile.name.split("/")[1], ": "]
                for item in fileData:
                    data.append(str(item) + ", ")
                result.writelines("\n")
                result.writelines(data)
        result.close()


findValue()
