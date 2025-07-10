from BaconShorClass import *
from ParityMatching import *
import sys
import time

#1:d_min 2:d_max 3:d_step 4:p_min 5:p_max 6:p_step 7:belief propagation 8:NoSamples 9:JobArrayID

seed_value = int(sys.argv[9])
random.seed(seed_value)
BeliefMatcingUsed = int(sys.argv[7])

d_min = int(sys.argv[1])
d_max = int(sys.argv[2])
d_step = int(sys.argv[3])

p_min = float(sys.argv[4])
p_max = float(sys.argv[5])
p_step = float(sys.argv[6])
NoOfSamples = int(sys.argv[8])

for n in range(d_min,d_max,d_step):
    tempstart = 0.0
    tempend = 0.0
    createBStime = 0, HNtime = 0, PMtime = 0, createBPtime = 0, BPtime = 0, initMatcherTime = 0, DecodeTime  = 0, succTime =0

    '''**** Initialise error parameters ***'''
    for pTotal in range(p_min,p_max,p_step):
        NoOfSucess = 0
        for samples in range(NoOfSamples):
            tempstart = time.time()
            '''* Initialise simulation parameters * '''
            BS = createBaconShorBase(n)
            tempend = time.time()#Recording end time.  
            createBStime += float(tempend - tempstart)#Calculating total time taken by the program.

            tempstart = time.time()
            #Insert errors
            #BS.InitHashingNoise(pTotal); #UNCOMMENT to choose hashing noise






