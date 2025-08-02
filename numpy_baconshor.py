
from itertools import product
from tabulate import tabulate
import itertools
from itertools import combinations
import random
import matplotlib.pyplot as plt
import numpy as np 

#false is no why y error
def create_grid(distance):
    grid = np.zeros((distance, distance), dtype=bool)
    return grid

#1 means error
def Print(grid,d):
    grid = grid.reshape((d, d))
    for row in grid.astype(int):
        print(" ".join(map(str, row)))

def Print_old(grid):
    for row in grid:
        for element in row:
            if element == True:
                print("1", end=" ")
            else:
                print("0", end=" ")
        print()

'''uses check_config_row and check_config_col to evaluate whether
the configuration is possible to be a Y logical'''
def check_config(grid):
    col = check_config_col(grid) #True if all column stabilizers work
    row = check_config_row(grid)# True if all row stabilizers work
    return col & row #returns True only if both are True

'''iterates over sets of columns and xors all values in that set. 
If there is an odd number of True's, the final value after xoring
for that set will be True, or otherwise False. A list stores all
of these final values and if all of them are False, the configuration
works for all columns and the function returns True'''
def check_config_col(grid):
    d = grid.shape[0]
    col_bool_values = []#all values should be False for the column stabilizers to work
    for i in range(d - 1):
        boolean = False
        # XOR across all rows for columns i and i+1
        for j in range(d):
            boolean ^= grid[j, i] ^ grid[j, i + 1]
        col_bool_values.append(boolean)
    
    return sum(val == False for val in col_bool_values) == d - 1
# for val in col_bool_values:
#         if val == False:
#             count+=1
#     if count == d-1:
#         return True
#     else:
#         return False
    
'''similar process as check_config_col, but instead iterates over rows'''
def check_config_row(grid):
    d = grid.shape[0]
    row_bool_values = []
    for i in range(d - 1):
        boolean = False
        # XOR across all columns for rows i and i+1
        for j in range(d):
            boolean ^= grid[i, j] ^ grid[i + 1, j]
        row_bool_values.append(boolean)

    return sum(val == False for val in row_bool_values) == d - 1

'''
stab is a grid with a stabilizer whose construction is described in construct_stabilizers_scipy_I.
It will be AND-ed with the grid given and then the resulting grid will be XORed.
Tis functoin vectorizes this so that we can check do this for all stabs in stabilizers'''
def check_stabilizer(grid, stab):
    result = np.bitwise_and(grid, stab)
    return  np.bitwise_xor.reduce(result.flatten()) 

    
'''takes in grid and a list of positions where to place y logicals
and inserts True in those positions
Assumes positions are given such that the topleft number is 1 and not 0'''
def add_y_error(grid,positions):
    d = grid.shape[0]  # assumes grid is square (d x d)
    for position in positions:
        if isinstance(position, int):
            row = (position - 1) // d
            col = (position - 1) % d
            grid[row, col] = True

'''returns only the number of possible Y logicals given d and w '''
def list_of_grids3_count(d, weight):
    possible_weight_locations = combinations(range(1, d**2 + 1), weight)
    num_of_valid_grids = 0

    for location_combo in possible_weight_locations:
        grid = create_grid(d)
        add_y_error(grid, location_combo)
        if check_config(grid):
            num_of_valid_grids += 1

    return num_of_valid_grids
'''returns the number of possible Y logicals given d and w and also prints out the grids'''
def list_of_grids3_grid(d, weight):
    possible_weight_locations = combinations(range(1, d**2 + 1), weight)
    num_of_valid_grids = 0

    for location_combo in possible_weight_locations:
        grid = create_grid(d)
        add_y_error(grid, location_combo)
        if check_config(grid):
            num_of_valid_grids += 1
            Print(grid)
            print()

    return num_of_valid_grids


def list_of_grids2(d, weight, breakupint, printgrid=False):
    num_of_possible_grids = 0
    iterator = 0
    this_lowlim = breakupint * 6e9
    this_highlim = this_lowlim + 6e9
    for possible_weight_location in combinations(range(1, (d**2) + 1), weight):
        if iterator >= this_lowlim and iterator < this_highlim:
            newgrid = create_grid(d)
            add_y_error(newgrid, possible_weight_location)
            if check_config(newgrid):
                num_of_possible_grids += 1
                if printgrid:
                    Print(newgrid)
                    print()
        iterator+=1
        if iterator >= this_highlim: return num_of_possible_grids
    return num_of_possible_grids

'''creates all possible grids for combinations of True and False
for any distance'''
def list_of_grids(d):
    num_cells = d ** 2

    # Generate all possible True/False combinations for d^2 positions
    y_logicals_combinations = product([True, False], repeat=num_cells)

    # Convert each flat tuple to a NumPy d×d array
    grids = [np.array(comb, dtype=bool).reshape((d, d)) for comb in y_logicals_combinations]

    return grids

'''got list of all possible k values from 0, d^2 -d and then from
there got a list of all possible number of y logicals'''   
def number_of_weights(d):
    max_k = (d**2 - d) // 2
    list_of_y = [2 * k + d for k in range(max_k + 1)]
    return list_of_y


def count_y_errors(grid):
    return np.count_nonzero(grid)

'''
function that takes in a list of grids and distance;
 creates a list containing values that represent
 how many y logicals are possible based on the k values; 
 and counts how many y logicals in a each grid and separates out the k values that 
 arent possible and then with the remaining,
makes a dictionary where keys are # of y logicals and values 
 are lists of grids where the configuration is possible
'''
def count_y_logicals_dict(listOfGrids, d):
    dictionary = {}
    possible_y_logicals = set(number_of_weights(d))  # convert to set for fast lookup

    for grid in listOfGrids:
        if check_config(grid):  # only consider valid configurations
            count = count_y_errors(grid)  # how many Y errors on this grid
            if count in possible_y_logicals:
                if count not in dictionary:
                    dictionary[count] = []
                dictionary[count].append(grid)

    return dictionary

        
    
'''function that takes that dictionary and prints out info in a nice format'''
def print_format(d,gridDictionary):
    print("Distance: ", d, "\n")
    for key in gridDictionary:
        print("weight: ", key, " | Number of y logicals: ", len(gridDictionary[key]))
        for i in range(len(gridDictionary[key])):
            Print(gridDictionary[key][i])
            print("")

def run(d):
    print_format(d,count_y_logicals_dict(list_of_grids(d), d))
    


def table(d, list_of_weights):
   print(f"d = {d}:\n")
   print("{:<10} {:<20}".format("WEIGHT", "# OF VALID GRIDS"))
   for w in list_of_weights:
    num = list_of_grids3_count(d, w)  # Use printgrid=True if you want to print grids
    print("{:<10} {:<20}".format(w, num))
    

'''creates a grid that adds an error on every position with probability p '''
def random_error_grid(d,p):
    # Create a d x d grid of False initially
    grid = create_grid(d)
    # Generate a d x d array of random floats in [0,1)
    random_vals = np.random.rand(d, d)
    # Set positions to True with probability p
    grid[random_vals < p] = True
    return grid

'''Create a dictionary of stabilizer measurements that gives the syndrome for each neighboring row and column'''
#used for gekko decoder, not numpy efficient right now
def construct_stabilizers(d, grid):
    Cs = {}  # Dictionary of stabilizer values

    # Create row and column stabilizers
    for i in range(d - 1):
        # Row stabilizers: vertical pairs
        row_indices = np.array([d * i + q for q in range(d)] + [d * (i + 1) + q for q in range(d)])
        Cs[tuple(row_indices)] = check_stabilizer(grid, row_indices)

        # Column stabilizers: horizontal pairs
        col_indices = np.array([d * q + i for q in range(d)] + [d * q + (i + 1) for q in range(d)])
        Cs[tuple(col_indices)] = check_stabilizer(grid, col_indices)

    return Cs

def construct_stabilizers_old(d):
    stabilizers = []
    for i in range(d - 1):
        # Row stabilizer: vertically adjacent rows
        row_stabilizer = np.concatenate([
            np.arange(d * i, d * i + d),
            np.arange(d * (i + 1), d * (i + 1) + d)
        ])
        stabilizers.append(row_stabilizer)
        col_stabilizer = np.concatenate([
            np.arange(d * 0 + i, d * d, d),       
            np.arange(d * 0 + (i + 1), d * d, d)  
        ])
        stabilizers.append(col_stabilizer)
    return stabilizers
'''returns a 3d numpy array that stores d by d grids of all of the stabilizers in such a way where
the location of each stabilizer is denoted by 1s on physical qubits, while the rest of the grid is 
filled with 0s'''
def construct_stabilizers_scipy_I(d):
    stabilizers = np.zeros((2 * (d - 1), d, d), dtype=int) # use 3d numpy array to store the grid of stabilizers

    for i in range(d - 1):
        # Row stabilizer: vertically adjacent rows
        stabilizers[2*i,i,:] = 1
        stabilizers[2*i,i+1,:] = 1

        # Column stabilizer: horizontally adjacent columns
        stabilizers[2*i +1,:, i] = 1
        stabilizers[2*i +1,:, i+1] = 1

    return stabilizers

'''list of syndrome measurement of each of those stabilizers in I'''
def construct_stabilizers_scipy_C(I, grid):
    C = np.empty(I.shape[0], dtype=int)
    for i, stab in enumerate(I):
        C[i] = 1-2* check_stabilizer(grid, stab)
        # print(i)
        # print(check_stabilizer(grid, stab))
        # print(C)
    return C



'''constructs the stabilizers for detecting x errors, 
which are just the z stabilizers in'''
def construct_stabilizers_scipy_x_errors_I(d):
    stabilizers = np.zeros((2 * (d - 1), d, d), dtype=int) # use 3d numpy array to store the grid of stabilizers

    for i in range(d - 1):
        # Row stabilizer: vertically adjacent rows
        stabilizers[2*i,i,:] = 1
        stabilizers[2*i,i+1,:] = 1
    return stabilizers


def construct_stabilizers_scipy_x_errors_C(I, grid):
    C = np.empty(I.shape[0], dtype=int)
    for i, stab in enumerate(I):
        C[i] = 1-2* check_stabilizer(grid, stab)
    return C


#for gekko
def solver_to_grid_gekko(d, solver_output: dict) -> np.ndarray:
    """
    Converts Gekko solver output (a dict of index: [value]) to a (d, d) NumPy grid.
    
    Example input:
        {0: [0.0], 1: [1.0], ..., 24: [0.0]}  # for d=5
    """
    # Extract the values in order of keys
    array = np.array([solver_output[i][0] for i in range(d*d)], dtype=int)
    return array.reshape((d, d))

#for scipy - changed because scipy output of the guess is different than gekko's
def solver_to_grid_scipy(d, solver_output: np.ndarray) -> np.ndarray:
    """
    Converts a flat 1D NumPy array from scipy.optimize.milp into a (d, d) grid.
    """
    return np.array(solver_output[:d*d]).reshape((d, d)).astype(int)


'''adds two grids using mod 2 addition'''
def add_grids(d, grid1, grid2):
    return np.bitwise_xor(grid1, grid2)


'''
checks is a logical error occurred by "adding" the error grid we created and 
the predicted error grid the MLE solver predicted. There is no logical error
if in the summed grid there is an even # of errors and if all the stabilizers 
are 1
'''
def solver_accuracy(d, grid, predicted):
    #edit this with the ylogical thing
    sum = add_grids(d, grid, predicted) #use numpy instead
    num_y_errors = count_y_errors(sum)
    return(num_y_errors % 2 == 0 and check_config(sum))

'''checks to see if the product of the original error grid or '''
def solver_accuracy_x_errors(d, grid, predicted):
    sum = add_grids(d, grid, predicted)
    #check to see if sum is an x logical: an even number of X errors in each row or an odd number of X errors in each row
    errors_per_row = np.count_nonzero(sum, axis=1)
    return np.all(errors_per_row % 2 == 0) and check_config_row(sum)


def plot(physical, logical,low_lim, high_lim, title="",  error_bars=None):
    fig,ax = plt.subplots(1,1,dpi=200,figsize = (4,3))
    if error_bars is not None:
        ax.errorbar(physical, logical, yerr=error_bars, capsize=3)
    else:
        ax.plot(physical, logical)

    ax.legend(fontsize=6)
    ax.set_ylim(low_lim, high_lim)
    ax.set_xlim(low_lim, high_lim)
    ax.set_xlabel("Physical Error Rate (p)")
    ax.set_ylabel("Logical Error Rate")
    plt.title(title)

def plot_multiple(distances, physical, logical,low_lim, high_lim, decoder, title="", error_bars=None):
    fig,ax = plt.subplots(1,1,dpi=200,figsize = (4,3))
    if error_bars is not None:
        for d, log, bars in zip(distances, logical, error_bars):
            ax.errorbar(physical, log, yerr=bars, capsize=3, label=f"{decoder} d={d}")
    else:
        for d, log in zip(distances, logical):
            ax.plot(physical, log, label=f"d={d}")

    ax.legend(fontsize=6)
    ax.set_yscale("log")
    ax.set_ylim(low_lim, high_lim)
    ax.set_xlim(low_lim, high_lim)
    ax.set_xlabel("Physical Error Rate (p)")
    ax.set_ylabel("Logical Error Rate")
    plt.title(title)

'''combines data into one file from the running parallel on cluster'''
def combine_parallel_data(num_files, file_prefix, file_suffix, output_file):
    files = [open(f"{file_prefix}{i}{file_suffix}", "r") for i in range(1, num_files + 1)]
    output = open(output_file, "a")

    # Process all lines together
    for lines in zip(*files):
        d, p, _, _ = lines[0].strip().split()
        d = int(d)
        p = float(p)

        total_count = 0
        total_shots = 0

        for line in lines:
            _, _, count, shots = line.strip().split()
            total_count += int(count)
            total_shots += int(shots)
        log_error_prob = total_count/total_shots
        std = np.sqrt(log_error_prob * (1 - log_error_prob)/total_shots)
        # print(std)
        output.write(f"{d} {p} {total_count} {total_shots} {std}\n")

    # Close files
    for f in files:
        f.close()
    output.close()

'''extracts data from input file and returns the lists of phys error probs, 
log error probs for each distance, the list of distances, and the lists of 
error bars for each phys error prob for each list of phys error probs'''
def print_from_csv(title):
    #Distance,Physical Error Probability, errors, shots, std
    distances=[]
    phys_probs={}
    log_probs = {}
    error_bars={}
    with open(title, "r") as f:
        for line in f:
            d, phys, count, shots, std = line.strip().split()
            d = int(d)
            phys, count, shots, std = float(phys), int(count), int(shots), float(std)
            if d not in distances:
                distances.append(d)  # Keep track of first appearance order
                phys_probs[d] = []
                log_probs[d] = []
                error_bars[d] = []
            phys_probs[d].append(phys)
            log_probs[d].append(count/shots)
            error_bars[d].append(std)
            
    phys_lists = [phys_probs[d] for d in distances]
    log_lists = [log_probs[d] for d in distances]
    errorbars_list = [error_bars[d] for d in distances]
    return phys_lists, log_lists, distances, errorbars_list

    # distances=[]
    # phys_probs={}
    # log_probs = {}
    # with open(title, "r") as f:
    #     for line in f:
    #         d, phys, log, error = line.strip().split(",")
    #         d = int(d)
    #         phys, log, error = float(phys), float(log), float(error)
    #         if d not in distances:
    #             distances.append(d)  # Keep track of first appearance order
    #             phys_probs[d] = []
    #             log_probs[d] = []
    #         phys_probs[d].append(phys)
    #         log_probs[d].append(log)
            
    # phys_lists = [phys_probs[d] for d in distances]
    # log_lists = [log_probs[d] for d in distances]
    # return phys_lists, log_lists, distances

# def print_from_csv_pm(title):
#     distances=[]
#     phys_probs={}
#     log_probs = {}
#     with open(title, "r") as f:
#         for line in f:
#             d, phys, count, shots = line.strip().split()
#             d = int(d)
#             phys, count, shots = float(phys), int(count), int(shots)
#             if d not in distances:
#                 distances.append(d)  # Keep track of first appearance order
#                 phys_probs[d] = []
#                 log_probs[d] = []
#             phys_probs[d].append(phys)
#             log_probs[d].append(count/shots)
            
#     phys_lists = [phys_probs[d] for d in distances]
#     log_lists = [log_probs[d] for d in distances]
#     return phys_lists, log_lists, distances
