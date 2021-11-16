from zxcvbn import zxcvbn

# files = ["1-Google.txt", "2-Amazon-50k.txt", "3-Facebook-50k.txt",
#          "5-Reddit-50k.txt", "6-Live-50k.txt", "10-Myshopify-50k.txt"]
files = ["1-Google.txt"]

newfiles = []

for file in files:
    originalFileName = file.split(".")
    newFileName = str(originalFileName[0]+"-zxcvbn."+originalFileName[1])
    newfiles.append(newFileName)

print(newfiles)


def zxcvbn_result(line, newfile):
    try:
        results = zxcvbn(line, user_inputs=[])
        # print(results)
        sequence = results["sequence"]
        score = ", score:"+str(results["score"])
        guess = ", guesses:"+str(sequence[0]["guesses"])
        pattern = ", pattern:"+str(sequence[0]["pattern"])
        password = "password:"+(str(line))
        data = [password, score, guess, pattern]
        newfile.writelines(data)
        newfile.writelines("\n")
    except:
        return print("Not Happening\n")


def compare(file, newfile):
    for line in file:
        zxcvbn_result(line.strip(), newfile)


for index, file in enumerate(files):
    currentFile = open(file)
    createNewFile = open(newfiles[index], "w")
    compare(currentFile, createNewFile)
    createNewFile.close()
    currentFile.close()
