#ifndef BM_FNC_H
#define BM_FNC_H

using namespace std;

struct ParityMatcherClass
{
	BaconShorBase CodeObject;

	vector<double>  qubitYBeliefs; // beliefs on qubits
	int n; 

	vector<double>  xChecksMatchingWeights; //weights associated with each row of qubits
    vector<double>  zChecksMatchingWeights; 

    bool* RowsToApplyZ;
	bool* ColsToApplyX;
	

	//Function declarations
	void GetMatchingWeights();
	void Decode();
	bool EvaluatedMatchingSuccess();



};

ParityMatcherClass initMatcher(BaconShorBase BS, vector<double> bqsY);




#endif
