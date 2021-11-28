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

currdirectory = os.getcwd()

print("Current working directory: " + currdirectory)

if not glob.glob("*.txt"):
    # anotha way: if len(glob.glob("*.txt")) == 0:
    sys.exit('No text files found in the cwd. Exiting...')

for file in os.listdir(currdirectory):
    # Find all the original policy text files, put them into the list
    # Can be *potentially* optimized
    if ("-zxcvbn" not in file) and (file.endswith(".txt") and (file.startswith("Results-"))):
        filesToBeDone.append(file)


def findAverageScore(score, index):
    return int(math.ceil(score / index))


def findAverageGuess(guess, index):
    return int(math.ceil(guess/index))


def findValue():
    score = 0
    guess = 0
    with open(resultFiles, 'w') as result:
        result.writelines("file_name, average_guess, average_score")
        for file in filesToBeDone:
            with open(file, 'r') as inputFile:
                for index, line in enumerate(inputFile):
                    if index == 0:
                        continue
                    splitString = line.split(",")
                    score += math.ceil(float(splitString[1]))
                    guess += math.ceil(float(splitString[2]))
                fileLength = len(open(file, 'r').readlines())
                print(guess)
                data = [inputFile.name,
                        ": ",
                        str(findAverageGuess(guess, fileLength)),
                        ", ",
                        str(findAverageScore(score, fileLength))]
                result.writelines("\n")
                result.writelines(data)
        result.close()


findValue()
