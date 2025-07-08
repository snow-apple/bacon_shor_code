#include "BaconShorClass.h"
#include "YOnlyBeliefPropagation.h"

#ifndef CE_FNC_H
#define CE_FNC_H

using namespace std;


struct CorrectionEvaluatorClass
{

	BaconShorBase CodeObject;
	BPArraysObject BPObject;

	int n;
	double pEY;


	//Function declaration
	bool IsCaseTrivial();
	bool DoRoundBeliefsSatisfySyndrome();
	bool BeliefPropCorrectionChecks(int maxRounds);


};


CorrectionEvaluatorClass createInitEvaluator(BaconShorBase BS, double pEy);


#endif