from core import *

tPriv = privateKeyH84()
tPub = publicKeyH84(tPriv.makeGPrime())
print "Encrypting bible.txt"
tPub.encryptFile("bible.txt")
print "Decrypting bible.txt.encode"
tPriv.decryptFile("bible.txt.encode")
