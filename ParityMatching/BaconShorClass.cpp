#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <vector>
#include<set>
#include "BaconShorClass.h"



using namespace std;

BaconShorBase createBaconShorBase(int n)
{
	BaconShorBase BaconShor;

	BaconShor.n = n;
	BaconShor.NoOfQubits = n*n; // start from top left and move across row then to row below
	BaconShor.NoOfZStabilizers = n-1; // for each pair of columns
    BaconShor.NoOfXStabilizers = n-1; // for each pair of rows
    BaconShor.NoOfStabilizers = 2*(n-1); // for each pair of rows
	BaconShor.NoOfErrors = 0; //how many errors there are
	BaconShor.ErrorPositions = std::vector<int>{};//where those errors are
	BaconShor.ErrorsPerRow = new int[n]();//initializes to 0
	BaconShor.ErrorsPerCol = new int[n]();//initializes to 0

    BaconShor.QubitYErrs = new bool[n*n]; // 0 of no Y err else 1
	for (int q = 0; q < n*n; q++)
        {
            BaconShor.QubitYErrs[q] = 0;
		}
    BaconShor.StabParities = new bool[2*(n-1)]; //X stabs indexed to row above, then Z stabs indexed to column to left


    return BaconShor;
}


vector<int> BaconShorBase::GetStabNeighbours(int a)
{
	vector<int> Neighbours(2*n, -1); // 2*n neighbours to each double row


	if (a < n-1) // X stabs
	{
		int rowAbove = a;
		int rowBelow = a+1;

		for (int c = 0; c < n; c++)
		{
			Neighbours[c] = rowAbove*n + c;
			Neighbours[c+n] = rowBelow*n + c;
		}

		return Neighbours; //indexes of neighbouring qubits		
	}
	else // Z stabs
	{
		a = a - (n-1);


		int colLeft = a;
		int colRight = a+1;

		for (int r = 0; r < n; r++)
		{
			Neighbours[r] = r*n + colLeft;
			Neighbours[r+n] = r*n + colRight;
		}

		return Neighbours; // indexes of neighbouring qubits

	}

	
}


void BaconShorBase::AllStabParityMeas()
{
	for (int a = 0; a < NoOfStabilizers; a++)
	{

		vector<int> StabNeighbouringQubits = GetStabNeighbours(a); //get enighbour indexes
			
		bool StabParity = 0;

		for (int q = 0; q< 2*n; q++)
		{
			StabParity = StabParity ^ QubitYErrs[StabNeighbouringQubits[q]];
		}

		StabParities[a] = StabParity;

	}



        // print stabilizer measurements


/*        cout << "X Stab checks (col) and Z stab checks (row)" << endl;

        for (int a = n-1; a < NoOfStabilizers; a++)
        {
            cout <<  StabParities[a] << " ";
        }

        cout <<  " " << StabParities[0] << endl;        

        for (int a = 1; a < n-1; a++)
        {
            cout <<  setw(n*2) << StabParities[a] << endl;
        }*/


}


vector<int> BaconShorBase::GetQubNeighbours(int q)
{
	vector<int> Neighbours(4, -1); // 4 neighbours to each qubit [above, below, left, right]

	int colQ = q % n;
	int rowQ = q /n;

	Neighbours[0] = rowQ - 1;
	Neighbours[1] = rowQ; 
	if (rowQ == n -1) 
	{
		Neighbours[1] = -1;
	}

	Neighbours[2] = (n-1) + colQ - 1;
	Neighbours[3] = (n-1) + colQ; 
	if (colQ == n-1) 
	{
		Neighbours[3] = -1;
	}
	if (colQ == 0) 
	{
		Neighbours[2] = -1;
	}
	return Neighbours;
	
}

void BaconShorBase::InitHashingNoise(double pTotal)
{
	    //cout <<  "Qubit States " << endl;

        // Insert errors 
        for (int q = 0; q < n*n; q++)
        {
            // QubitYErrs[q] = 0;

            double err =  (double)rand() / (double)RAND_MAX;

            if (err < pTotal)
            {
                QubitYErrs[q] = 1;
				NoOfErrors += 1;
				ErrorPositions.push_back(q);
				ErrorsPerRow[q / n] += 1;
				ErrorsPerCol[q % n] += 1;
            }

            // print errors

/*            cout << QubitYErrs[q] << "  " ;
            if (q % n == n-1)
            {
                cout << endl;
            }*/
        }  
}

//change this function to take in a list
void BaconShorBase::InitCombinatorialErr(const vector<int>& sampleIndices)
{
	    //cout <<  "Qubit States " << endl;

        // Insert errors 
		for(int idx: sampleIndices){
            QubitYErrs[idx] = 1;
			NoOfErrors += 1;
			ErrorPositions.push_back(idx);
			ErrorsPerRow[idx / n] += 1;
			ErrorsPerCol[idx % n] += 1;
		}
            // print errors

/*            cout << QubitYErrs[q] << "  " ;
            if (q % n == n-1)
            {
                cout << endl;
            }*/
        
}








