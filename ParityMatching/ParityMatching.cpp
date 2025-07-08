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
#include "ParityMatching.h"



ParityMatcherClass initMatcher(BaconShorBase BS, vector<double> bqsY)
{
	ParityMatcherClass Matcher;

	Matcher.CodeObject = BS;
	Matcher.qubitYBeliefs = bqsY;

	Matcher.n = BS.n;

	Matcher.xChecksMatchingWeights = vector<double> (BS.n, 0);
    Matcher.zChecksMatchingWeights = vector<double> (BS.n, 0);

    Matcher.RowsToApplyZ = new bool[BS.n]; // 0 of no Y err req to be applied else 1
    Matcher.ColsToApplyX = new bool[BS.n]; 

    return Matcher;
}


void ParityMatcherClass::GetMatchingWeights()
{
	//these matching weights are calculated to first order, assuming only one error per row/column
	//POSSIBLE IMPROVEMENT: calculate upto nth order

	//do x Checks first (assoc with double rows)
	for (int row = 0; row < n; row++)
	{
		double oneMinusrowbqs = 1;
		for (int col = 0; col < n; col++)
		{
			oneMinusrowbqs = oneMinusrowbqs * (1 - qubitYBeliefs[row*n + col]);
		}
		for (int col = 0; col < n; col++)
		{
			xChecksMatchingWeights[row] += oneMinusrowbqs * qubitYBeliefs[row*n + col] / (1 - qubitYBeliefs[row*n + col]);
		}

		xChecksMatchingWeights[row] = -log(xChecksMatchingWeights[row]/(1-xChecksMatchingWeights[row]));
		
	}

	// now do z Checks (assoc with double columns)
	for (int col = 0; col < n; col++)
	{
		double oneMinuscolbqs = 1;
		for (int row = 0; row < n; row++)
		{
			oneMinuscolbqs = oneMinuscolbqs * (1 - qubitYBeliefs[row*n + col]);
		}
		for (int row = 0; row < n; row++)
		{
			zChecksMatchingWeights[col] += oneMinuscolbqs * qubitYBeliefs[row*n + col] / (1 - qubitYBeliefs[row*n + col]);
		}

		zChecksMatchingWeights[col] = -log(zChecksMatchingWeights[col]/(1-zChecksMatchingWeights[col]));
		
	}

/*	cout << endl << " Looking at x Check Matching Weights:" << endl;
	for (int i = 0; i < n; i++)
	{
		cout << setw(3) << i  << ":  " << setw(8) << xChecksMatchingWeights[i] << " " << endl;
	}	
	cout << endl << " Looking at z Check Matching Weights:" << endl;
	for (int i = 0; i < n; i++)
	{
		cout << setw(3) << i  << ":  " << setw(8) << zChecksMatchingWeights[i] << " " << endl;
	}	*/


}

void ParityMatcherClass::Decode()
{
	int XRepCodeAssignedMatching[n]; //assign each qubit row to matching 0 or 1
	int ZRepCodeAssignedMatching[n];

	int currXMatching = 0, currZMatching = 0;

	double bothXRepMatchingWeights[2] = {0.0};
	double bothZRepMatchingWeights[2] = {0.0};

	int numRowsAssignedtoXRepMatch[2] = {0};
	int numRowsAssignedtoZRepMatch[2] = {0};


	//first do Xmatching (vertical repetition code)
	for (int qubrow = 0; qubrow < n; qubrow++) //determine matching weights
	{
		bothXRepMatchingWeights[currXMatching] += xChecksMatchingWeights[qubrow];

		//cout <<  currXMatching << "matching weight updated to " <<  bothXRepMatchingWeights[currXMatching] << endl;

		XRepCodeAssignedMatching[qubrow] = currXMatching;
		numRowsAssignedtoXRepMatch[currXMatching]++;

		if (qubrow < (n-1) and CodeObject.StabParities[qubrow] == 1)
		{
			currXMatching = currXMatching ^ 1;
		}
	}

	//next do Zmatching (horizontal repetition code)
	for (int qubcol = 0; qubcol < n; qubcol++) //determine matching weights
	{
		bothZRepMatchingWeights[currZMatching] += zChecksMatchingWeights[qubcol];

		//cout <<  currZMatching << "matching weight updated to " <<  bothZRepMatchingWeights[currZMatching] << endl;

		ZRepCodeAssignedMatching[qubcol] = currZMatching;
		numRowsAssignedtoZRepMatch[currZMatching]++;

		if (qubcol < (n-1) and CodeObject.StabParities[(n-1) + qubcol] == 1)
		{
			currZMatching = currZMatching ^ 1;
		}
	}

	//get corrections
	for (int qubrc = 0; qubrc < n; qubrc++)
	{
		RowsToApplyZ[qubrc] = XRepCodeAssignedMatching[qubrc] ^ (bothXRepMatchingWeights[0] < bothXRepMatchingWeights[1]);
		ColsToApplyX[qubrc] = ZRepCodeAssignedMatching[qubrc] ^ (bothZRepMatchingWeights[0] < bothZRepMatchingWeights[1]);
		cout << RowsToApplyZ[qubrc] ;
		cout << ColsToApplyX[qubrc] ;

	}

	

}





bool ParityMatcherClass::EvaluatedMatchingSuccess()
{
	bool AllRowsHaveZs = true, AllColsHaveXs = true;

	for (int qubrow = 0; qubrow < n; qubrow++) //do Zs per row first
	{
		bool RowZParity = RowsToApplyZ[qubrow];
		for(int qubcol = 0; qubcol < n; qubcol++)
		{
			RowZParity = RowZParity ^ CodeObject.QubitYErrs[qubrow*n+qubcol];
		}
		if (RowZParity == 0) {AllRowsHaveZs = false;}

	}

	for (int qubcol = 0; qubcol < n; qubcol++) //now do Xs per col
	{
		bool ColXParity = ColsToApplyX[qubcol];
		for(int qubrow = 0; qubrow < n; qubrow++)
		{
			ColXParity = ColXParity ^ CodeObject.QubitYErrs[qubrow*n+qubcol];
		}
		if (ColXParity == 0) {AllColsHaveXs = false;}

	}

	if (AllColsHaveXs or AllRowsHaveZs) {return false;}
	return true;

}
