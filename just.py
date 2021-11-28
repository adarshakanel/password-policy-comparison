from zxcvbn import zxcvbn

def zxcvbn_result(lineInput):
	#:param - input password, which is passed as a string
	#:return - list containing results from performing 'zxcvbn' on input
	try:
		resultsRow = []
		#Empty list initialized for storing the output 
		results = zxcvbn(lineInput)
		#sequence = results["sequence"]
		tempPass = results['password']
		#The input password (obtained by extracting line by line from the policy text files), type: String
		tempScore = results['score']
		#Integer from 0-4, 0 being too guessable, 4 being very unguessable, type: Integer
		tempCalcTime = results['calc_time']
		tempCalcTime = float(tempCalcTime.total_seconds())
		#how long it took zxcvbn to calculate an answer, in milliseconds. Since tempCalcTime is originally a 
		# datetime.TimeDelta type, converted to number of seconds contained in the duration using total_seconds()
		tempGuesses = results['guesses']
		#estimated guesses needed to crack password, type: Float

		#Following are estimations of different scenarios to 'crack' the password
		tempOnlineRL = float(results['crack_times_seconds']['online_throttling_100_per_hour'])
		# online attack on a service that ratelimits password auth attempts.
		tempOnlineNoRL = float(results['crack_times_seconds']['online_no_throttling_10_per_second'])
		#  online attack on a service that doesn't ratelimit, or where an attacker has outsmarted ratelimiting.
		tempOfflineFH = float(results['crack_times_seconds']['offline_fast_hashing_1e10_per_second'])
		#offline attack with user-unique salting but a fast hash function like SHA-1, SHA-256 or MD5
		tempOfflineSH = float(results['crack_times_seconds']['offline_slow_hashing_1e4_per_second'])
		## offline attack. assumes multiple attackers, proper user-unique salting, and a slow hash function w/ moderate work factor, such as bcrypt, scrypt, PBKDF2.

		resultsRow = [(tempPass), (tempScore), (tempGuesses), (tempCalcTime), 
					  (tempOnlineRL), (tempOnlineNoRL), (tempOfflineFH), (tempOfflineSH)]
		return resultsRow
		#order: Password,Score,Guesses,CalcTime,OnlineRateLimited,OnlineNoRateLimited,OfflineFastHash,OfflineSlowhash

	except Exception: 
		#Yeah idk about this part but oh well, should be helpful still
		print("Error:\n")
		print(traceback.format_exc())
		traceback.print_exc()