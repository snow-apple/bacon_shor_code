#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <vector>
#include<set>
#include "YOnlyBeliefPropagation.h"
#include "BaconShorClass.h"
#include "CorrectionEvaluator.h"



CorrectionEvaluatorClass createInitEvaluator(BaconShorBase BS, double pEy)
{
	CorrectionEvaluatorClass Evaluator;

	Evaluator.n = BS.n;
	Evaluator.pEY = pEy;

	Evaluator.CodeObject = BS;
	Evaluator.BPObject = createBPArrays(pEy, BS);

    return Evaluator;
}

bool CorrectionEvaluatorClass::IsCaseTrivial()
{
	bool AllParities0 = true;
	bool AllQubits0 = true;

	for (int a = 0; a < CodeObject.NoOfStabilizers; a++)
	{
		if (CodeObject.StabParities[a] == 1) { AllParities0 = false; }
	}

	if (AllParities0)
	{
		for (int q = 0; q < CodeObject.NoOfQubits; q++)
		{
			if (CodeObject.QubitYErrs[q] == 1) { AllQubits0 = false; }			
		}

		if (AllQubits0) { return true; }
	}

	return false;
}


bool CorrectionEvaluatorClass::DoRoundBeliefsSatisfySyndrome()
{

	BaconShorBase DummyBS = createBaconShorBase(n);

	for (int q = 0; q < DummyBS.NoOfQubits; q++)
	{
		DummyBS.QubitYErrs[q] = 0;

		if (BPObject.logPqsY[q] > 0)
		{
			DummyBS.QubitYErrs[q] = 1;
		}
	}

	//Measure checks
    DummyBS.AllStabParityMeas();

    for (int a = 0; a < DummyBS.NoOfStabilizers; a++)
    {
    	if (DummyBS.StabParities[a] != CodeObject.StabParities[a])
    	{
    		return false;
    	}
    }

	return true;

}


bool CorrectionEvaluatorClass::BeliefPropCorrectionChecks(int maxRounds)
{

	bool succeeded = false;

	if (IsCaseTrivial()) { succeeded=true; }

	else
	{
		bool continueBP = true;
		bool solutionFound = false;
		int BProunds = 0;

		if (maxRounds == 0)
		{
			for (int q = 0; q < CodeObject.NoOfQubits; q++) { BPObject.bqsY[q] = pEY;}
			continueBP = false; //no chance of solution found since all bqs are < 0.5			
		}

		while(continueBP)
        {
            BPObject.GetChecktoQubitMessages();
            BPObject.GetQubittoCheckMessages();
            BPObject.GetQubitBeliefs();
        	BPObject.GetPredictedWeights();

        	solutionFound = DoRoundBeliefsSatisfySyndrome();

        	BProunds++;

        	if (BProunds == maxRounds or solutionFound)
        	{
        		continueBP = false;
        		if (solutionFound) {succeeded = true;}
        	}

        }

	}

	if (!succeeded)
	{
            // print errors
		for (int q = 0; q < CodeObject.NoOfQubits; q++)
		{

            //cout << CodeObject.QubitYErrs[q] << "  " ;
            if (q % n == n-1)
            {
                //cout << endl;
            }	
        }
	}

	return succeeded;

}
