from core import *

m = np.matrix([
[0,0,0,0]
],dtype=int)
print "Message  => \t",m
tPriv = privateKeyH84()
tPub = publicKeyH84(tPriv.makeGPrime())
ct = tPub.encrypt(m)
print "Cipher   => \t",ct
mt = tPriv.decrypt(ct)
print "Message' => \t",mt
if np.array_equal(m, mt):
    print "RESULT => Text equals"
else:
    print "RESULT => Text no equals"
