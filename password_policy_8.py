from zxcvbn import zxcvbn

file = "4-Yahoo-50K.txt"
newFile = "8-Yahoo.txt"


def compare(file, newfile):
    for line in file:
        try:
            results = zxcvbn(line, user_inputs=[])
            score = results["score"]
            if score > 0:
                newfile.writelines(line)
        except:
            next


currentFile = open(file)
createNewFile = open(newFile, "w")
compare(currentFile, createNewFile)
createNewFile.close()
currentFile.close()
