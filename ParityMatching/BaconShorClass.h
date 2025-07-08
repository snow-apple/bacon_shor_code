#ifndef BSC_FNC_H
#define BSC_FNC_H

using namespace std;

struct BaconShorBase
{
	int n; 
	int NoOfQubits;
    int NoOfZStabilizers;
    int NoOfXStabilizers;
    int NoOfStabilizers;

	bool* QubitYErrs;
	bool* StabParities;



	//Function declarations


	// Function to measure star operator about vertex 'Vertex'
	vector<int> GetStabNeighbours(int a);
	void AllStabParityMeas();
	vector<int> GetQubNeighbours(int q);
	void InitHashingNoise(double pTotal);
	void InitCombinatorialErr(const vector<int>& sampleIndices);

};

BaconShorBase createBaconShorBase(int n);
int nChoosek( int n, int k );



#endif
