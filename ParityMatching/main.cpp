#include <iostream>
#include <iomanip>      
#include <ctime>
#include <fstream>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <vector>
#include <sstream>
#include "BaconShorClass.h"
#include "YOnlyBeliefPropagation.h"
#include "CorrectionEvaluator.h"
#include "ParityMatching.h"

using namespace std;

int main(int argc, char** argv)
{   


    // main 1:d_min 2:d_max 3:d_step 4:p_min 5:p_max 6:p_step 7:R_e 8:NoSamples

    // * Set seed *
    srand(atoi(argv[9]));
    bool BeliefMatcingUsed = atoi(argv[7]);
    
    for (int n = atoi(argv[1]); n < atoi(argv[2]); n+=atoi(argv[3]))
    {

    clock_t tempstart, tempend;
     double createBStime = 0, HNtime = 0, PMtime = 0, createBPtime = 0, BPtime = 0, initMatcherTime = 0, DecodeTime  = 0, succTime =0;
 

    // **** Initialise error parameters ***
    for (double pTotal = atof(argv[4]); pTotal < atof(argv[5]); pTotal+=atof(argv[6]))
    {
   

    int NoOfSamples = atoi(argv[8]);  //
    int NoOfSuccess = 0;
    for (int samples = 0; samples < NoOfSamples; samples++)
    {


        tempstart = clock();
        // * Initialise simulation parameters * 
        BaconShorBase BS = createBaconShorBase(n); 
        tempend = clock(); // Recording end time.             
        createBStime += double(tempend - tempstart); // Calculating total time taken by the program.


        tempstart = clock();
        //Insert errors
        // BS.InitHashingNoise(pTotal); //UNCOMMENT to choose hashing noise


        int x = 25; // numbers from 0 to 24
        vector<vector<int>> combinations;

        // for (int i = 0; i < x; i++) {
        //     combinations.push_back({i});
        // }
        for (int i = 0; i < x; i++) {
            for (int j = i + 1; j < x; j++) {
                combinations.push_back({i, j});
            }
        }
        // for (int i = 0; i < x; i++) {
        //     for (int j = i + 1; j < x; j++) {
        //         for (int k = j + 1; k < x; k++) {
        //             combinations.push_back({i, j, k});
        //     }
        // }
        // }
        BS.InitCombinatorialErr(combinations[atoi(argv[9])]); //UNCOMMENT to choose combinatorial noise
        cout << "Original Error Grid:\n";
        for (int i = 0; i < BS.NoOfQubits; i++) {
            cout << BS.QubitYErrs[i] << " ";
            if ((i + 1) % n == 0) cout << endl; // new line every n elements
        }
        
        tempend = clock(); // Recording end time.             
        HNtime += double(tempend - tempstart); // Calculating total time taken by the program.


        tempstart = clock();
        //Measure checks
        BS.AllStabParityMeas();
        tempend = clock(); // Recording end time.             
        PMtime += double(tempend - tempstart); // Calculating total time taken by the program.


        bool succeeded = 0;
        tempstart = clock();
        CorrectionEvaluatorClass BPArrays;
        if (BeliefMatcingUsed)
        {
            // Initialise belief propagation arrays object
            BPArrays = createInitEvaluator(BS, pTotal);
            tempend = clock(); // Recording end time.             
            createBPtime += double(tempend - tempstart); // Calculating total time taken by the program.


            //Conduct belief propagation and check if solns match syndrome
            int maxRounds = 2*0;

            tempstart = clock();
            succeeded = BPArrays.BeliefPropCorrectionChecks(maxRounds);
            //cout << "BP convergence: " << succeeded << endl;          
        }
        tempend = clock(); // Recording end time.             
        BPtime += double(tempend - tempstart); // Calculating total time taken by the program.


        if (!succeeded)
        {
            tempstart = clock();
            ParityMatcherClass ParityMatcher;

            if (BeliefMatcingUsed)
            {
                ParityMatcher = initMatcher(BS, BPArrays.BPObject.bqsY);    
            }
            else
            {
                int numQs = BS.n * BS.n;
                vector<double> bqs(numQs, pTotal);
                ParityMatcher = initMatcher(BS, bqs);                  
            }
            
            ParityMatcher.GetMatchingWeights();
            tempend = clock(); // Recording end time.             
            initMatcherTime += double(tempend - tempstart); // Calculating total time taken by the program.

            tempstart = clock();
            ParityMatcher.Decode();
            tempend = clock(); // Recording end time.             
            DecodeTime += double(tempend - tempstart); // Calculating total time taken by the program.

            tempstart = clock();
            succeeded = ParityMatcher.EvaluatedMatchingSuccess();
            cout << "Successed?:\n";
            if(!succeeded){
                cout << "No\n";
            }
            else{
                cout << "Yes\n";
            }
             tempend = clock(); // Recording end time.             
            succTime += double(tempend - tempstart); // Calculating total time taken by the program.

            //cout << "Matching success: " << succeeded << endl << endl;
        }

        NoOfSuccess = NoOfSuccess + int(succeeded);


        // *** Begin decoding *** 
			                       
    
    }

    int FailCount = NoOfSamples - NoOfSuccess;

    cout << n << " " << pTotal << " "  << FailCount << " " << NoOfSamples << endl;


    }

    //cout << "Create BS    : " << createBStime << endl;
    //cout << "Hashing Noise: " << HNtime << endl;
    //cout << "Parity Meas  : " << PMtime << endl;
    //cout << "Create BP Arr: " << createBPtime << endl;
    //cout << "Do BP        : " << BPtime << endl;
    //cout << "Init Matcher : " << initMatcherTime << endl;
    //cout << "Decode + MW  : " << DecodeTime << endl;
    //cout << "Eval Success : " << succTime << endl;
    }

    return 0;
}
