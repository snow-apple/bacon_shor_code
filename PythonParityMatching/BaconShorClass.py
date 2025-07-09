from dataclasses import dataclass, field
import random

@dataclass
class BaconShorBase:
    n: int
    NoOfQubits: int
    NoOfZStabilizers: int
    NoOfXStabilizers: int
    NoOfStabilizers: int
    NoOfErrors: int
    ErrorPositions: list[int]
    QubitYErrs: list[bool]
    StabParities: list[bool]
    ErrorsPerRow: list[int]
    ErrorsPerCol: list[int]

def createBaconShorBase(n):
    BaconShor = BaconShorBase()
    BaconShor.n = n
    BaconShor.NoOfQubits = n*n #start from top left and move across row then to row below
    BaconShor.NoOfZStabilizers = n-1 #for each pair of columns
    BaconShor.NoOfXStabilizers = n-1 #for each pair of rows
    BaconShor.NoOfStabilizers = 2*(n-1)# for each pair of rows
    BaconShor.NoOfErrors = 0#how many errors there are
    BaconShor.ErrorPositions = []#where those errors are
    BaconShor.ErrorsPerRow = [0]*n#initializes to 0
    BaconShor.ErrorsPerCol = [0]*n#initializes to 0

    BaconShor.QubitYErrs = [0] * (n*n) #0 of no Y err else 1

    BaconShor.StabParities = [None]*(2*(n-1)) #X stabs indexed to row above, then Z stabs indexed to column to left

    return BaconShor

def GetStableNeighbours(a, BaconShor):
    n = BaconShor.n
    Neighbors = [-1]*(2*n)# 2*n neighbours to each double row

    if a < n-1:
        rowAbove = a
        rowBelow = a+1
        for c in range(n):
            Neighbors[c] = rowAbove*n + c
            Neighbors[c+n] = rowBelow*n + c
        return Neighbors
    else:
        a = a - (n-1)

        colLeft = a
        colRight = a+1

        for r in range(n):
            Neighbors[r] = r*n + colLeft
            Neighbors[r+n] = r*n + colRight
        return Neighbors
    
def AllStabParityMeas(BaconShor):
    for a in range(BaconShor.NoOfStabilizers):
        StabNeighbouringQubits = GetStableNeighbours(a, BaconShor) #get neighbour indexes

        StabParity = 0
        for q in range(2*BaconShor.n):
            StabParity = StabParity ^ BaconShor.QubitYErrs[StabNeighbouringQubits[q]]
        
        BaconShor.StabParities[a] = StabParity



def GetQubNeighbours(q,BaconShor):
    Neighbors = [-1]*4 #4 neighbours to each qubit [above, below, left, right]
    n = BaconShor.n

    colQ = q % n
    rowQ = q /n

    Neighbors[0] = rowQ - 1
    Neighbors[1] = rowQ
    if rowQ == n-1:
        Neighbors[1] = -1
    
    Neighbors[2] = (n-1) + colQ - 1
    Neighbors[3] = (n-1) + colQ
    if colQ == n-1:
        Neighbors[3] = -1
    if colQ == 0:
        Neighbors[2] = -1

    return Neighbors

def InitHashingNoise(pTotal, BaconShor):
    n = BaconShor.n
    for q in range(n*n):
        err = random.random()

        if err <pTotal:
            BaconShor.QubitYErrs[q] = 1
            BaconShor.NoOfErrors += 1
            BaconShor.ErrorPositions.append(q)
            BaconShor.ErrorsPerRow[q / n] += 1
            BaconShor.ErrorsPerCol[q % n] += 1

def InitCombinatorialErr(sampleIndices, BaconShor):
    n = BaconShor.n
    for idx in sampleIndices:
        BaconShor.QubitYErrs[idx] = 1
        BaconShor.NoOfErrors += 1
        BaconShor.ErrorPositions.append(idx)
        BaconShor.ErrorsPerRow[idx / n] += 1
        BaconShor.ErrorsPerCol[idx % n] += 1


















 
