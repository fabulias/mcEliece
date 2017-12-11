from __future__ import print_function
from colorprint import *

from core import *

debug = False

for ix in range(0, 10):
    m = np.array([np.random.randint(2, size=4)])
    print ("Message  => \t",m)
    tPriv = privateKey()
    if debug :
        tPriv.printKeys()
    tPub = publicKey(tPriv.makeGPrime())
    ct = tPub.encrypt(m)
    print ("Recived   => \t",ct)
    mt = tPriv.decrypt(ct)
    print ("Message' => \t", mt)
    if np.array_equal(m, mt):
        print ('RESULT', 'Text equals', color='green', end='\n', sep=' => ')
    else:
        print ('RESULT', 'Text no equals', color='red', end='\n', sep=' => ')
