from zxcvbn import zxcvbn
file1 = open("1-Google.txt")
createNewFile1 = open("1-Google-zxcvbn.txt", "w")


def zxcvbn_result(line):
    try:
        results = zxcvbn(line, user_inputs=[])
        print(results)
        sequence = results["sequence"]
        score = results["score"]
        guess = sequence[0]["guesses"]
        pattern = sequence[0]["pattern"]
        print("sequence: ", sequence)
        print("guess: ", guess)
        print("pattern: ", pattern)
        print("score: ", score, "\n")
    except:
        return print("Not Happening\n")


def compare(files):
    # for file in files:
    count = 0
    for line in files:
        # to test
        if count > 500:
            break
        else:
            count += 1
        # print(input)
        zxcvbn_result(line)


compare(file1)
