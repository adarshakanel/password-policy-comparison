from zxcvbn import zxcvbn
results = zxcvbn('JohnSmith123', user_inputs=['John', 'Smith'])

# y = json.loads(results)
sequence = results["sequence"]

guesses = sequence[0]["guesses"]
token = sequence[0]["token"]
rank = sequence[0]["rank"]
base_guesses = sequence[0]["base_guesses"]

print("token: ", token, " rank ", rank,
      " guesses: ", guesses, " base_guesses ", base_guesses)
