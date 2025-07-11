import sys
import numpy_baconshor
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds, OptimizeResult
import matplotlib.pyplot as plt
import csv
import time
from typing import List, Union
def mle_decoder_bs(M : int, I : List[List[int]], C : List[int], p : Union[List[float], float]) -> OptimizeResult:
    """
    Solves the MLE decoder problem using a MILP solver.

    Parameters:
        - M: Number of binary variables E_j.
        - I: List of lists. I[i] is the set of errors E_j which flip the check C_i
        - C: Constraint values C_i.
        - p: List of probabilities p_j for each E_j.

    Returns:
        - result: The result object from scipy.optimize.milp.
        
    """
    # Validate input data
    N = len(I)
    assert len(C) == N, "Length of C must be N"

    #can remove
    if np.isscalar(p):
        p = np.full(M, p)
    # elif type(p) is List:
    #     assert len(p) == M, "Length of p must be M"
    # else:
    #     raise ValueError('p must be a float or a list of floats')

    # Idea: The decision variable x contains both E_j and K_i values.
    # i.e. x = [E_1, ..., E_M, K_1, ..., K_N]
    # The scipy milp solver minimizes <c, x> where c is the objective function coefficients. 
    # We can ignore the constant log(1-p_j) in the objective function.

    # Construct the objective function coefficients, by default set the K_i coefficients to zero
    # Note the minus sign for the E_i coeffs because the solver minimizes the objective function
    c = np.array([-np.log(p_j) + np.log(1 - p_j) for p_j in p] + [0]*N) #remove since assuming all p are same

    # Construct equality constraints matrix (constraints are Ax = b)
    A_eq = np.zeros((N, M + N)) # N constraints, (M + N) variables
    b_eq = []
    for i in range(N):

        # Constraint for the check, C_i is: \sum_{Ej in I_i} E_j - 2K_i = (1 - C_i)/2
        # where I_i is the set of errors [...,E_j,...] that flip the check C_i
        
        # Firstly, set the matrix elements to pick out the appropriate E_j values
        for j in I[i]:
            if j >= M:
                raise ValueError(f"E_j index {j} exceeds M-1")
            A_eq[i, j] = 1

        # Next, set matrix elements to pick out the corresponding K_i
        A_eq[i, M + i] = -2

        # Lastly, compute the right-hand side (1 - C_i)/2
        b_eq.append((1 - C[i]) / 2)

    # Define constraints (equality constraints)
    constraints = LinearConstraint(A=A_eq, lb=b_eq, ub=b_eq)

    # Bounds: E_j: binary (0-1), K_i: integer >=0
    bounds = Bounds(lb = [0]*M + [0]*N,
                    ub = [1]*M + [np.inf]*N)

    # Integrality: Both E_j and K_i are integers within bounds (i.e. 1)
    integrality = [1]*(M + N)  

    # Solve the MILP
    res = milp(c           = c,
               constraints = constraints,
               integrality = integrality,
               bounds      = bounds)
    
    return M, N, res

def Print_result(M,N,result):
    guess = []
    if result.success:
        print("Optimization successful.")
        print(">> Maximum objective value:", -result.fun)  # Convert back to maximization
        print(">> Optimal E_j values:")
        for j in range(M):
            print(f"\t E_{j+1} = {round(result.x[j])}")
            guess.append(round(result.x[j]))
        print(">> Optimal K_i values:")
        for i in range(N):
            print(f"\t K_{i+1} = {int(result.x[M + i])}")
    else:
        print("No optimal solution found.")
        print("Status:", result.message)
        print("Details:", result.get("message", "No additional information"))

    return guess

def print_result(M,N,result):
    guess = []
    if result.success:
        # print("Optimization successful.")
        # print(">> Maximum objective value:", -result.fun)  # Convert back to maximization
        # print(">> Optimal E_j values:")
        # for j in range(M):
        #     # print(f"\t E_{j+1} = {round(result.x[j])}")
        #     guess.append(round(result.x[j]))
        return np.round(result.x[:M]).astype(int)
        # print(">> Optimal K_i values:")
        # for i in range(N):
        #     print(f"\t K_{i+1} = {int(result.x[M + i])}")
    else:
        print("No optimal solution found.")
        # print("Status:", result.message)
        # print("Details:", result.get("message", "No additional information"))


n = len(sys.argv)
if n != 9:
    print("Not enough arguments")
    exit()

for M in range(int(sys.argv[1]) ,int(sys.argv[2]), int(sys.argv[3])):#iterates over d values
    #construct stabilizer - I
    I = numpy_baconshor.construct_stabilizers_scipy_I(M)
    I_decoder = numpy_baconshor.construct_stabilizers_old(M)
    filename = sys.argv[8] + ".txt"
    with open(filename, "a") as file:
        for p in np.arange(float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])):#iterates over p values
            count = 0
            shots = int(sys.argv[7])
            starttime = time.monotonic()
            averagerandomerrorgridtime = 0
            averageconstructstabilizertime = 0
            averagedecodertime = 0
            averageaccuracytime = 0
            for i in range(int(shots)):#iterates over number of samples/shots
                shotstarttime = time.monotonic()
                grid = numpy_baconshor.random_error_grid(M,p)
                randomerrorgridtime = time.monotonic()
                averagerandomerrorgridtime+= (randomerrorgridtime - shotstarttime)
                #construct C
                C = numpy_baconshor.construct_stabilizers_scipy_C(I,grid)
                constructstabilizertime = time.monotonic()
                averageconstructstabilizertime += (constructstabilizertime - randomerrorgridtime)
                guess = print_result(*mle_decoder_bs(M**2,I_decoder,C,p))
                decodertime = time.monotonic()
                averagedecodertime += (decodertime -constructstabilizertime)
                if(numpy_baconshor.solver_accuracy(M,grid,numpy_baconshor.solver_to_grid_scipy(M,guess)) != True):
                    count+=1
                accuracytime = time.monotonic()
                averageaccuracytime+= (accuracytime - decodertime)
            endtime = time.monotonic()
            # log_error_prob = count/shots
            # std = np.sqrt(log_error_prob * (1 - log_error_prob) / shots)
            print(M, p, count, shots, endtime - starttime, averagerandomerrorgridtime/shots,  averageconstructstabilizertime/shots, averagedecodertime/shots,averageaccuracytime/shots, sep=" ", file=file)#use time to see if changin stabilizer makes a diff
            #see how much time each function takes - package??- py-spy, speedscope
