from core import *
import os

tPriv = privateKey()
tPub = publicKey(tPriv.makeGPrime())
print "Encrypting bible.txt"
tPub.encryptFile("bible.txt")
print "Decrypting bible.txt.encode"
tPriv.decryptFile("bible.txt.encode")
os.system("diff bible.txt bible.txt.encode.decoded")
