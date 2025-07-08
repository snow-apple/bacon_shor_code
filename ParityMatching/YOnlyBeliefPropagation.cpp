#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <vector>
#include<set>
#include<algorithm>
#include "YOnlyBeliefPropagation.h"
#include "BaconShorClass.h"


using namespace std;


BPArraysObject createBPArrays(double pEY, BaconShorBase BS)
{
	BPArraysObject AllMessages;

	AllMessages.CodeObject = BS;
	AllMessages.n = BS.n;
	AllMessages.pEY = pEY;
	AllMessages.pEI = 1 - pEY;


    AllMessages.mcqsY = vector<vector<double> >(2*(BS.n - 1), vector<double>(2 * BS.n));


    AllMessages.mqcsY = vector<vector<double> >(BS.n * BS.n, vector<double>(4, pEY)); // 4 are [above, below, left, right]
    AllMessages.mqcsI = vector<vector<double> >(BS.n * BS.n, vector<double>(4, 1 - pEY));

    AllMessages.bqsY = vector<double> (BS.n * BS.n, 1);
    AllMessages.logPqsY = vector<double> (BS.n * BS.n, 1);


    return AllMessages;
}

int BPArraysObject::MQCIndex(int q, int a) //where are checks relative to qubits [above, below, left, right]
{

	if (a < n-1) // X stab
	{
		if (a ==  q / n - 1) // indexed to same row above
		{
			return 0; 
		}
		else if (a == q / n )
		{
			return 1; //next row, 2nd element
		}

	}
	else // Z stab
	{
		a = a - (n-1);
		if (a ==  q % n - 1) // indexed to same column to left
		{
			return 2; 
		}
		else if (a == q % n )
		{
			return 3; //next column, 4th element
		}
	}

	return -1;


}

int BPArraysObject::MCQIndex(int a, int q) // where are qubits relative to checks
{

	if (a < n-1) // X stab
	{
		if (a ==  q / n) // indexed to same row above
		{
			return q % n; // column number 
		}
		else if (a + 1 == q / n )
		{
			return n + q %n; //next row
		}

	}
	else
	{ 
		a = a - (n-1);

		if (a ==  q % n) // indexed to same column to left
		{
			return q / n; // row number 
		}
		else if (a + 1 == q % n )
		{
			return n + q / n; //next column
		}
	}

	return -1;


}

void BPArraysObject::GetChecktoQubitMessages()
{
	for (int a = 0; a < CodeObject.NoOfStabilizers; a++)
	{

		vector<int> allNeighbours = CodeObject.GetStabNeighbours(a);
		int numNeighbours = allNeighbours.size();

		for ( int i = 0; i < numNeighbours; i++)
		{
			CalculateMcqs(a, allNeighbours[i], allNeighbours);
		}

	}


/*	for (int i = 0; i < CodeObject.NoOfStabilizers; i++)
	{
		for (int j = 0; j < 2*n; j++)
		{
			cout << setw(10) << mcqsY[i][j] << " ";
		}
		cout << endl;
	}*/

}

void BPArraysObject::CalculateMcqs(int a, int q, vector<int> allNeighbours)
{

	allNeighbours.erase(remove(allNeighbours.begin(), allNeighbours.end(), q), allNeighbours.end());

	int numQs = allNeighbours.size();
	vector<double> allMqcProducts(int(pow(2,numQs)),1);
	vector<bool> NoOfYsParity(int(pow(2,numQs)), 0 );

	for (int i = 0; i < numQs; i++)
	{
		int currQubit = allNeighbours[i];

		for (int j = 0; j < pow(2,numQs); j++)
		{
			bool currLocParity = bool(int(j / pow(2,(numQs - i - 1))) % 2);

			NoOfYsParity[j] = NoOfYsParity[j] ^ currLocParity;

			if (currLocParity== 0)
			{
				allMqcProducts[j] = allMqcProducts[j] * mqcsI[currQubit][MQCIndex(currQubit,a)];
			}
			else
			{
				allMqcProducts[j] = allMqcProducts[j] * mqcsY[currQubit][MQCIndex(currQubit,a)];
			}
		}
	}

	double EvenYErrsSum = 0;
	double OddYErrsSum = 0;

	for (int i = 0; i < pow(2,numQs); i++)
	{
		if (NoOfYsParity[i] == 0) //even number of Y errs
		{
			EvenYErrsSum = EvenYErrsSum + allMqcProducts[i];
		}
		else
		{
			OddYErrsSum = OddYErrsSum + allMqcProducts[i];
		}
	}


	if (CodeObject.StabParities[a]) // if the check is lit up
	{
		mcqsY[a][MCQIndex(a,q)] = EvenYErrsSum / (OddYErrsSum + EvenYErrsSum);
	}
	else
	{
		mcqsY[a][MCQIndex(a,q)] = OddYErrsSum / (OddYErrsSum + EvenYErrsSum);
	}


}


void BPArraysObject::GetQubittoCheckMessages()
{
	for (int q = 0; q < CodeObject.NoOfQubits; q++)
	{
		//cout << "Looking at neighbours of qubit " << q << ": " << endl;

		vector<int> allNeighbours = CodeObject.GetQubNeighbours(q);

		for ( int i = 0; i < 4; i++)
		{
			if (allNeighbours[i] != -1)
			{
				//cout << "     to check " << allNeighbours[i] << ": " << endl;
				CalculateMqcs(q, allNeighbours[i], allNeighbours);			
			}

		}

	}


/*	for (int i = 0; i < CodeObject.NoOfQubits; i++)
	{
		cout << setw(3) << i  << ":  ";
		for (int j = 0; j < 4; j++)
		{
			cout << setw(10) << mqcsY[i][j] << " ";
		}
		cout << endl;
	}*/

}


void BPArraysObject::CalculateMqcs(int q, int a, vector<int> allNeighbours)
{

	allNeighbours.erase(remove(allNeighbours.begin(), allNeighbours.end(), a), allNeighbours.end());

	double YErrMessage = pEY;
	double IErrMessage = pEI;

	for (int i = 0; i < 3; i++)
	{
		int currAncilla = allNeighbours[i];

		//cout << "             using info to  " << currAncilla << ",  " << endl;

		if (currAncilla != -1)
		{
			//cout <<"              is index " <<  MCQIndex(currAncilla,q) << " with "<<  mcqsY[currAncilla][MCQIndex(currAncilla,q)] << " ";
			YErrMessage = YErrMessage * mcqsY[currAncilla][MCQIndex(currAncilla,q)];
			IErrMessage = IErrMessage * (1-mcqsY[currAncilla][MCQIndex(currAncilla,q)]);
			//cout << "updating to (" << YErrMessage << ", " << IErrMessage << ")" << endl;
		}
		
	}

	//cout << "     Updating MQC index (" << q << "," << MQCIndex(q,a) << ")" << endl;

	mqcsY[q][MQCIndex(q,a)] = YErrMessage/(YErrMessage+IErrMessage);
	mqcsI[q][MQCIndex(q,a)] = IErrMessage/(YErrMessage+IErrMessage);


}


void BPArraysObject::GetQubitBeliefs()
{
	for (int q = 0; q < CodeObject.NoOfQubits; q++)
	{

		vector<int> allNeighbourStabs = CodeObject.GetQubNeighbours(q);

		double YErrMessage = pEY;
		double IErrMessage = pEI;

		for (int i = 0; i < 4; i++)
		{
			int currAncilla = allNeighbourStabs[i];

			if (currAncilla != -1)
			{
				YErrMessage = YErrMessage * mcqsY[currAncilla][MCQIndex(currAncilla,q)];
				IErrMessage = IErrMessage * (1-mcqsY[currAncilla][MCQIndex(currAncilla,q)]);
			}
		}

		bqsY[q] = YErrMessage/(YErrMessage+IErrMessage);
	}


/*	cout << endl << " Looking at final qubit beliefs:" << endl;
	for (int i = 0; i < CodeObject.NoOfQubits; i++)
	{
		cout << setw(3) << i  << ":  " << setw(8) << bqsY[i] << " " << endl;
	}*/

}

void BPArraysObject::GetPredictedWeights()
{
	for (int q = 0; q < CodeObject.NoOfQubits; q++)
	{
		logPqsY[q] = log(bqsY[q]/(1-bqsY[q]));
	}


/*	cout << endl << " Looking at final qubit beliefs:" << endl;
	for (int i = 0; i < CodeObject.NoOfQubits; i++)
	{
		cout << setw(3) << i  << ":  " << setw(8) << bqsY[i] << " " << endl;
	}	*/
}