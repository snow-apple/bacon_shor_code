#include "BaconShorClass.h"

#ifndef BP_FNC_H
#define BP_FNC_H

using namespace std;


struct BPArraysObject
{

	BaconShorBase CodeObject;
	int n;
	double pEY;
	double pEI;


    vector<vector<double> > mcqsY; //messages from checks to qubits


    vector<vector<double> >  mqcsY; //messages from qubits to checks
    vector<vector<double> >  mqcsI; 

    vector<double>  bqsY; // beliefs on qubits
    vector<double>  logPqsY; 


	//Function declarations
	int MQCIndex(int q, int a); //where are checks relative to qubits
	int MCQIndex(int a, int q); // where are qubits relative to checks

	void GetChecktoQubitMessages(); //mcq generation step
	void CalculateMcqs(int a, int q, vector<int> allNeighbours);

	void GetQubittoCheckMessages(); //mqc generation step
	void CalculateMqcs(int q, int a, vector<int> allNeighbours);

	void GetQubitBeliefs();
	void GetPredictedWeights();



};

BPArraysObject createBPArrays(double pEy, BaconShorBase BS);



#endif