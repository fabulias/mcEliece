# Core Library Utilities
import numpy as np
import pickle
import os.path
import random
import csv
from utils import *

class privateKeyH84:
	"""Datastructure to represent our Private Key"""
	def __init__(self,S=None,P=None):
		"""Initalizer that will set S & P matricies to random if not given values"""
		#Hamming 8,4 in standard
		self.G = np.matrix([
		[1,0,0,0,0,1,1,1],
		[0,1,0,0,1,0,1,1],
		[0,0,1,0,1,1,0,1],
		[0,0,0,1,1,1,1,0]
		], dtype=int)
		self.H = np.matrix([
		[0,1,1,1,1,0,0,0],
		[1,0,1,1,0,1,0,0],
		[1,1,0,1,0,0,1,0],
		[1,1,1,0,0,0,0,1]
		], dtype=int)

		#Can create these from known values, otherwise random
		if S == None:
			self.S = modTwo(genSMatrix(4))
		else:
			self.S = S

		if P == None:
			self.P = modTwo(genPMatrix(8))
		else:
			self.P = P

	def printCode(self):
		"""Canonical print to screen function"""
		print "S: \n" + str(self.S) + "\n"
		print "P: \n" + str(self.P) + "\n"
		print "GPrime: \n" + str(self.makeGPrime()) + "\n"

	def writeKeyToFile(self, keyFile):
		"""Saves key to a pickle file"""
		try:
			pickle.dump(self, open(keyFile,"wb"))
		except:
			print "Could not save key file to: ",keyFile
			exit(1)

	def readKeyFromFile(self,keyFile):
		"""Reads key from a pickle file"""
		try:
			newPriv = pickle.load( open(keyFile,"rb"))
			self.S = newPriv.S
			self.P = newPriv.P
		except:
			print "Could not load key file from: ",keyFile
			exit(1)

	def makeGPrime(self):
		"""Creates the GPrime encrytion Matrix"""
		return modTwo(self.S*self.G*self.P)

	def decrypt(self,c):
		"""When given cipher text will decode to message"""
		cHat = c * modTwo(self.P.I.astype(int))
		m = bitFlip(cHat,syndromeLookup(self.H,modTwo(self.H*cHat.T)))
		return modTwo(m[0,0:4] * modTwo(self.S.I.astype(int)))

	def decryptFile(self,f):
		"""Will decrypt whole file"""
		cf = open(f,"rb")
		cb1 = cf.read(1)
		cb2 = cf.read(1)

		mf = open(f+".decoded","wb")

		while cb1 and cb2:

			#First Byte of Cipher Text
			c_1 = '{0:08b}'.format(ord(cb1))[0:8]
 			c1_l = []
			m1 = ""
			for s in c_1:
				c1_l.append(s)
			c_1_m = np.matrix(c1_l,dtype=int)

			d1 = self.decrypt(c_1_m)

			for d in range(0,d1.size):
				m1 += str(d1.item(d))

			#Second Byte of Cipher Text
			c_2 = '{0:08b}'.format(ord(cb2))[0:8]
 			c2_l = []
			m2 = ""
			for s in c_2:
				c2_l.append(s)
			c_2_m = np.matrix(c2_l,dtype=int)

			d2 = self.decrypt(c_2_m)

			for d in range(0,d2.size):
				m2 += str(d2.item(d))

			#print m1+m2
			mf.write(chr(int(m1+m2,2)))
			cb1 = cf.read(1)
			cb2 = cf.read(1)

		mf.close()
		cf.close()

	def dnaFileDecrypt(self,f,dlu):
		"""Decrypts a file that has been turned into a DNA representation"""
		cf = open(f,"r")
		c1 = cf.readline().strip("\n")
		c2 = cf.readline().strip("\n")

		mf = open(f+".decoded","w")

		while c1 and c2:
			m1 = ""
			m2 = ""
			mat1 = np.matrix(" ".join(dlu.lookDNADecrypt(c1)),dtype=int)
			mat2 = np.matrix(" ".join(dlu.lookDNADecrypt(c2)),dtype=int)
			d1 = self.decrypt(mat1)
			d2 = self.decrypt(mat2)
			for d in range(0,d1.size):
				m1 += str(d1.item(d))

			for d in range(0,d2.size):
				m2 += str(d2.item(d))

			mf.write(chr(int(m1+m2,2)))
			c1 = cf.readline().strip("\n")
			c2 = cf.readline().strip("\n")

		mf.close()
		cf.close()

#### Public Key H84 ####
class publicKeyH84:
	"""Public Key Data Structure"""
	def __init__(self,GPrime):
		self.GPrime = GPrime

	def printCode(self):
		"""Canonical print to screen"""
		print "GPrime: \n" + str(self.GPrime) + "\n"

	def writeKeyToFile(self, keyFile):
		"""Saves key to a pickle file"""
		try:
			pickle.dump(self, open(keyFile,"wb"))
		except:
			print "Could not save key file to: ",keyFile
			exit(1)

	def readKeyFromFile(self,keyFile):
		"""Reads key from a pickle file"""
		try:
			newPub = pickle.load( open(keyFile,"rb"))
			self.GPrime = newPub.GPrime
		except:
			print "Could not load key file from: ",keyFile
			exit(1)

	def encrypt(self,m):
		"""When given a message will encode"""
		#Error vector will be random
		z = random.randint(1,7)
		c = bitFlip(modTwo(m*self.GPrime),z)
		return c

	def encryptFile(self,f):
		"""Encrypts a whole file"""

		mf = open(f,"rb")
		m = mf.read(1)

		cf = open(f+".encode","wb")

		while m:
			#First half byte of message text
			m_1 = '{0:08b}'.format(ord(m))[0:4]
			m1_l = []
			c1 = ""
			for s in m_1:
				m1_l.append(s)
			m_1_m = np.matrix(m1_l,dtype=int)

			d1 = self.encrypt(m_1_m)
			for d in range(0,d1.size):
				c1 += str(d1.item(d))
			cf.write(chr(int(c1,2)))

			#Second half byte of message text
			m_2 = '{0:08b}'.format(ord(m))[4:]
			m2_l = []
			c2 = ""
			for s in m_2:
				m2_l.append(s)
			m_2_m = np.matrix(m2_l,dtype=int)

			d2 = self.encrypt(m_2_m)
			for d in range(0,d2.size):
				c2 += str(d2.item(d))
			cf.write(chr(int(c2,2)))

			m = mf.read(1)

		cf.close()
		mf.close()
