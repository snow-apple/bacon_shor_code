import pm
import baconshor
import sys
import numpy as np

#1:d_start 2:d_end 3:d_step 4:p_start 5:p_end 6:p_step 7:#shots 8:name
n = len(sys.argv)
if n != 9:
    print("Not enough arguments")
    exit()

for M in range(int(sys.argv[1]) ,int(sys.argv[2]), int(sys.argv[3])):#iterates over d values
    #construct stabilizer - I
    I = baconshor.construct_stabilizers_scipy_I(M)
    filename = sys.argv[8] + ".txt"
    with open(filename, "a") as file:
        for p in np.arange(float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])):#iterates over p values
            count = 0
            shots = int(sys.argv[7])

            for i in range(int(shots)):#iterates over number of samples/shots
              
                grid = baconshor.random_error_grid(M,p)
                print("Error Grid: ")
                baconshor.Print(grid)
                #construct C
                C = baconshor.construct_stabilizers_scipy_C(I,grid) #dont need to construct I for every shot 
            
                #Get Lengths
                r1,r2,c1,c2 = pm.get_matchings(C)
                
                #5. Identify minimum weight rows and cols
                lowest_matching_weights = pm.get_lowest_matching(r1,r2,c1,c2)

                #6. Applying correction based on intersection 
                if len(lowest_matching_weights["row"]) == len(lowest_matching_weights["col"]):
                    predicted_grid = pm.intersection_correction(M,lowest_matching_weights)
                else:
                    predicted_grid = pm.broadcasting_correction(M,lowest_matching_weights)
                print("Predicted Grid: ")
                baconshor.Print(predicted_grid)
                #7. Check if correction produced logical error or not
                if(baconshor.solver_accuracy(M,grid,predicted_grid) != True):
                    count+=1
                    print("fail")
                
            # log_error_prob = count/shots
            # std = np.sqrt(log_error_prob * (1 - log_error_prob) / shots)
            print(M, p, count, shots, sep=" ", file=file)#use time to see if changin stabilizer makes a diff


