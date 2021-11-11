from zxcvbn import zxcvbn


def zxcvbn_result(input):
    results = zxcvbn('JohnSmith123', user_inputs=['John', 'Smith'])
    sequence = results["sequence"]
    guesses = sequence[0]["guesses"]
    token = sequence[0]["token"]
    rank = sequence[0]["rank"]
    base_guesses = sequence[0]["base_guesses"]
    print("token: ", token, ", rank ", rank,
          ", guesses: ", guesses, ", base_guesses ", base_guesses)


def compare(files):
    for file in files:
        for input in file:
            print(input)
            zxcvbn_result(input)


compare([["password1", "password2"], ["password3", "password4"]])
