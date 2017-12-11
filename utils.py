import numpy as np

def genSMatrix(k):
	sMaybe = np.matrix(np.random.randint(0,2,k*k).reshape(k,k).astype(int))
	while True:
		try:
			sMaybe.getI()
			return sMaybe
		except:
			sMaybe = np.matrix(np.random.randint(0,2,k*k).reshape(k,k).astype(int))

def genPMatrix(n,keep=False):
	p = np.identity(n, dtype=int)
	if keep:
		return np.matrix(p).reshape(n,n)
	else:
		return np.matrix(np.random.permutation(p))

def modTwo(C):
	D = C.copy()
	D.fill(2)
	return np.remainder(C,D)

def bitFlip(C,n):
	if n == 0:
		return C
	if n == -1:
		index = random.randint(1,C.size -1)
	else:
		index = n

	if C[0,index-1] == 1:
		C[0,index-1] = 0
	else:
		C[0,index-1] = 1
	return C

def all_zeros(d):
	zc = 0
	for x in d:
		if x == 0:
			zc += 1
	if zc == len(d):
		return True
	else:
		return False

def syndromeLookup(H,d):
	t = H.T.tolist()
	s = d.T.tolist()[0]

	if all_zeros(s):
		return 0
	try:
		return t.index(s) + 1
	except:
		return 0

def checkOldGuesses(oG,newGuess):
	for s in oG:
		if np.array_equal(newGuess.A1,s.A1):
			return False
		else:
			return True

def makeString(matrix):
	message = ""
	for m in matrix.A1:
		if m == "[":
			pass
		elif m == "]":
			pass
		elif m == " ":
			pass
		else:
			message += str(m)
	return message
