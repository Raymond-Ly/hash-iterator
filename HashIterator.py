import sys, os, hashlib

if __name__ == "__main__":
	# Read input file from first argument
	if len(sys.argv) < 2:
		sys.exit("First argument must be a path to a file")

	if not os.path.isfile(sys.argv[1]):
		sys.exit("Input file specified does not exist")

	try:
		inputFile = open(sys.argv[1], "r")
		input = inputFile.read()
		inputFile.close()
	except Exception as err:
		sys.exit(err)
	
	# File should contain a string, a comma, and an integer, so parse it
	seedLen = input.rfind(",")
	if seedLen == -1:
		sys.exit("Input file is malformed - no comma found")
		
	seed = input[:seedLen]
	try:
		zeroesToDiscard = int(input[seedLen+1:])
		if zeroesToDiscard < 0:
			sys.exit("Zeroes to discard must not be negative")
		elif zeroesToDiscard > 16:
			sys.exit("Zeroes to discard cannot be greater than 16")
			
		zeroesStr = "".zfill(zeroesToDiscard)
	except ValueError:
		sys.exit("Expected integer after final comma in input file")
		
	# Our output variable will always be 10 chars long, a period represents an unsolved position
	output = "." * 10
		
	print("Solving for seed '" + seed + "', discarding " + str(zeroesToDiscard) + " zeroes (" + zeroesStr + ")...")
	
	iteration = 0
	foundChars = 0
		
	while 1:
		iteration += 1
		hash = hashlib.md5(seed+str(iteration)).hexdigest()
		if hash[:zeroesToDiscard] == zeroesStr:	# Discard anything that doesn't start with specified number of zeroes
			
			try:
				outputCharPos = int(hash[zeroesToDiscard]) # Discard non-numeric results (i.e. hex a-f)
			except ValueError:
				continue
			
			charToUse = iteration % 32
			if output[outputCharPos] == ".": # If we haven't solved this position
				output = output[:outputCharPos] + hash[charToUse] + output[outputCharPos+1:]
				foundChars += 1
				print("This hash: " + hash + ", current output: " + output + " (" + "char: " + hash[charToUse] + " pos: " + str(outputCharPos) + " idx: " + str(charToUse) + " iter: " + str(iteration) + ")")
				if foundChars == 10:
					try:
						outputFile = open(sys.argv[1]+".answer", "w+")
						outputFile.write(output)
						outputFile.close()
					except:
						sys.exit(err)
					sys.exit(output)
