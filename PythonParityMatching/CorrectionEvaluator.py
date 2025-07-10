from dataclasses import dataclass, field
from BaconShorClass import *


@dataclass
class CorrectionEvaluatorClass:
    CodeObject: BaconShorBase 

    n: int
    pEY: float


def createInitEvaluator(BS, pEy):
    Evaluator = CorrectionEvaluatorClass()
    Evaluator.n = BS.n
    Evaluator.pEY = pEy
    Evaluator.CodeObject = BS
    return Evaluator

def IsCaseTrivial(Evaluator):
    return 0
    



    





