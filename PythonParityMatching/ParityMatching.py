from dataclasses import dataclass, field
from BaconShorClass import *
import math

@dataclass
class ParityMatcherClass:
    CodeObject: BaconShorBase 
    qubitYBeliefs: list[float]
    n: int

    xChecksMatchingWeights: list[float]
    zChecksMatchingWeights: list[float]

    RowsToApplyZ: list[bool]
    ColsToApplyX: list[bool]

def initMatcher(BS, bqsY):
    Matcher = ParityMatcherClass()

    Matcher.CodeObject = BS
    Matcher.qubitYBeliefs = bqsY

    Matcher.n = BS.n

    Matcher.xChecksMatchingWeights = [0.0] * BS.n
    Matcher.zChecksMatchingWeights = [0.0] * BS.n

    Matcher.RowsToApplyZ = [False] * BS.n #0 of no Y err req to be applied else 1
    Matcher.ColsToApplyX = [False] * BS.n 

    return Matcher

def GetMatchingWeights(Matcher):
    #do x Checks first (assoc with double rows)
    n = Matcher.n
    for row in range(n):
        oneMinusrowbqs = 1
        for col in range(n):
            oneMinusrowbqs = oneMinusrowbqs * (1 - Matcher.qubitYBeliefs[row*n + col])
        for col in range(n):
            Matcher.xChecksMatchingWeights[row] += oneMinusrowbqs * Matcher.qubitYBeliefs[row*n + col] / (1 - Matcher.qubitYBeliefs[row*n + col])
        Matcher.xChecksMatchingWeights[row] = -math.log(Matcher.xChecksMatchingWeights[row]/(1-Matcher.xChecksMatchingWeights[row]))

    #now do z Checks (assoc with double columns)
    for col in range(n):
        oneMinuscolbqs = 1
        for row in range(n):
            oneMinuscolbqs = oneMinuscolbqs * (1 - Matcher.qubitYBeliefs[row*n + col])
        for row in range(n):
            Matcher.zChecksMatchingWeights[col] += oneMinuscolbqs * Matcher.qubitYBeliefs[row*n + col] / (1 - Matcher.qubitYBeliefs[row*n + col])
        Matcher.zChecksMatchingWeights[col] = -math.log(Matcher.zChecksMatchingWeights[col]/(1-Matcher.zChecksMatchingWeights[col]))
    
def Decode(Matcher):
    n = Matcher.n
    XRepCodeAssignedMatching = [None]*n #assign each qubit row to matching 0 or 1
    ZRepCodeAssignedMatching = [None]*n

    currXMatching = 0
    currZMatching = 0

    bothXRepMatchingWeights = [0.0, 0.0]
    bothZRepMatchingWeights = [0.0, 0.0]

    numRowsAssignedtoXRepMatch = [0,0]
    numRowsAssignedtoZRepMatch = [0,0]

    #first do Xmatching (vertical repetition code)
    for qubrow in range(n): #determine matching weights
        bothXRepMatchingWeights[currXMatching] += Matcher.xChecksMatchingWeights[qubrow]
        XRepCodeAssignedMatching[qubrow] = currXMatching
        numRowsAssignedtoXRepMatch[currXMatching] +=1

        if qubrow < (n-1) and  Matcher.CodeObject.StabParities[qubrow] == 1:
            currXMatching = currXMatching ^ 1

    #next do Zmatching (horizontal repetition code)
    for qubcol in range(n):#determine matching weights
        bothZRepMatchingWeights[currZMatching] += Matcher.zChecksMatchingWeights[qubcol]
        ZRepCodeAssignedMatching[qubcol] = currZMatching
        numRowsAssignedtoZRepMatch[currZMatching] += 1

        if qubcol < (n-1) and Matcher.CodeObject.StabParities[(n-1) + qubcol] == 1:
            currZMatching = currZMatching ^ 1
    
    #get corrections
    for qubrc in range(n):
        Matcher.RowsToApplyZ[qubrc] = XRepCodeAssignedMatching[qubrc] ^ (bothXRepMatchingWeights[0] < bothXRepMatchingWeights[1])
        Matcher.ColsToApplyX[qubrc] = ZRepCodeAssignedMatching[qubrc] ^ (bothZRepMatchingWeights[0] < bothZRepMatchingWeights[1])
		#print(RowsToApplyZ[qubrc]) 
		#print(ColsToApplyX[qubrc] )

def EvaluatedMatchingSuccess(Matcher):
    n = Matcher.n
    AllRowsHaveZs = True
    AllColsHaveXs = True

    for qubrow in range(n):#do Zs per row first
        RowZParity = Matcher.RowsToApplyZ[qubrow]
        for qubcol in range(n):
            RowZParity = RowZParity ^ Matcher.CodeObject.QubitYErrs[qubrow*n+qubcol]
        if RowZParity == 0:
            AllRowsHaveZs = False
    for qubcol in range(n):#now do Xs per col
        ColXParity = Matcher.ColsToApplyX[qubcol]
        for qubrow in range(n):
            ColXParity = ColXParity ^ Matcher.CodeObject.QubitYErrs[qubrow*n+qubcol]
        if ColXParity == 0:
            AllColsHaveXs = False
    if AllColsHaveXs or AllRowsHaveZs:
        return False
    else:
        return True








    








        








