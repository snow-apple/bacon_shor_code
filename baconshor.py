
from itertools import product
from tabulate import tabulate
import itertools
from itertools import combinations
import random
import matplotlib.pyplot as plt
import numpy as np 

#false is no why y error
def create_grid(distance):
    grid = [[False for _ in range(distance)] for _ in range(distance)]
    return grid

#1 means error
def Print(grid):
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
    d = len(grid)
    col_bool_values = []#all values should be False for the column stabilizers to work
    for i in range(d-1):
        boolean = False
        for j in range(d):
            boolean = boolean ^ grid[j][i] ^ grid[j][i+1]
        col_bool_values.append(boolean) #False if that stabilizer box works
    # print(col_bool_values)
    count = 0
    for val in col_bool_values:
        if val == False:
            count+=1
    if count == d-1:
        return True
    else:
        return False
    
'''similar process as check_config_col, but instead iterates over rows'''
def check_config_row(grid):
    d = len(grid)
    row_bool_values = []#all values should be False for the column stabilizers to work
    for i in range(d-1):
        boolean = False
        for j in range(d):
            boolean = boolean ^ grid[i][j] ^ grid[i+1][j]
        row_bool_values.append(boolean) #False if that stabilizer box works
    # print(row_bool_values)
    count = 0
    for val in row_bool_values:
        if val == False:
            count+=1
    if count == d-1:
        return True
    else:
        return False

'''Takes in a grid and a list of indexes on the grid that represent what physical qubits make up the stabilizer
and outputs the stabilizer measurement, 1 or -1. Uses notation for grid that starts at 0 at top left index'''
def check_stabilizer(grid, positions):
    d = len(grid)
    boolean = False

    for p in positions:
        row = (p)//d
        col = (p)%d
        # print(str(row) + ", "+ str(col)+ ": "+str(grid[row][col]))
        boolean = boolean ^ grid[row][col]
    if boolean == False:
        return 1
    else:
        return -1
    
'''takes in grid and a list of positions where to place y logicals
and inserts True in those positions
Assumes positions are given such that the topleft number is 1 and not 0'''
def add_y_error(grid,positions):
    d = len(grid)#find length of grid
    for position in positions:
        if type(position) == int:
            row = (position - 1) // d #gives row
            col = (position - 1 )% d #gives col
            # print(row,col)
            grid[row][col] = True

def list_of_grids3(d, weight, printgrid=False):
    possible_weight_locations = list(combinations(list(range(1, (d**2)+1)),weight))
    possible_grids = []
    num_of_possible_grids=0
    for i in range(len(possible_weight_locations)):
        newlist = list(possible_weight_locations[i])
        newgrid = create_grid(d)
        add_y_error(newgrid, newlist)
        if(check_config(newgrid)):
            num_of_possible_grids += 1
            possible_grids.append(newgrid)
            if(printgrid):
                Print(newgrid)
                print()
    return num_of_possible_grids
    
def list_of_grids2(d, weight, breakupint, printgrid=False):
    num_of_possible_grids = 0
    iterator = 0
    for possible_weight_location in combinations(range(1, (d**2) + 1), weight):
        this_lowlim = breakupint * 6e9
        this_highlim = this_lowlim + 6e9
        if iterator >= this_lowlim and iterator < this_highlim:
            newlist = list(possible_weight_location)
            newgrid = create_grid(d)
            add_y_error(newgrid, newlist)
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
    grid_size = d  # dxd grid
    num_cells = grid_size ** 2  # d^2 cells in the grid

    # Generate all combinations of True/False (logical Y placements) for d^2 positions
    y_logicals_combinations = list(product([True, False], repeat=num_cells))

    # Convert the entire list of tuples into a list of lists of lists
    y_logicals_combinations_as_lists = [
        [list(y_logicals_combinations[i][j:j + grid_size]) for j in range(0, len(y_logicals_combinations[i]), grid_size)]
        for i in range(len(y_logicals_combinations))
    ]
    # for grid in y_logicals_combinations_as_lists:
    #     print(grid)
    return y_logicals_combinations_as_lists

'''got list of all possible k values from 0, d^2 -d and then from
there got a list of all possible number of y logicals'''   
def number_of_y_errors_from_distance(d):
    list_of_k  = []
    for i in range((d**2 - d)//2 +1):
        list_of_k.append(i*2)
    list_of_y = []
    for i in range(len(list_of_k)):
        list_of_y.append(list_of_k[i]+d)
    return list_of_y


def count_y_errors(grid):
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == True:
                count +=1
    return count

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
    possible_y_logicals = number_of_y_errors_from_distance(d)
    for grid in listOfGrids:
        if check_config(grid):
            count = count_y_errors(grid) 
            if count in possible_y_logicals:
                if count in dictionary:#add grids to dictonary based on how many y logicals
                    dictionary[count].append(grid)
                else:
                    dictionary[count] = [grid]
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
    dict_to_table = {}
    count = 0
    for w in list_of_weights:
        num = list_of_grids2(d,w, True)
        dict_to_table[count] = [str(w), str(num)]
        count +=1
    print("d="+str(d)+":\n")
    print("{:<10} {:<10}".format('WEIGHT', '# OF COMBINATIONS'))
    for key, value in dict_to_table.items():
        weight, num_of_combinations = value
        print("{:<10} {:<10}".format(weight, num_of_combinations))
    

'''creates a grid that adds an error on every position with probability p '''
def random_error_grid(d,p):
    grid = create_grid(d)
    list1 = list(range(1, d**2+1))
    # print(list1)
    #where to add y errors
    error_list = []
    for i in range(len(list1)):
        # print("hi")
        if random.random() < p:
            error_list.append(list1[i])
    # print(error_list)
    add_y_error(grid,error_list)
    return grid

'''Create a dictionary of stabilizer measurements that gives the syndrome for each neighboring row and column'''
#used for gekko decoder
def construct_stabilizers(d, grid):
    total = []
    for i in range(d-1):
        listrow=[]
        listcol=[]
        for q in range(d):
            listrow.append(d*i +q)
            listrow.append((d)*(i+1) + q)
            listcol.append(d*q +i)
            listcol.append(d*q +(i+1))
        total.append(listrow)
        total.append(listcol) 
    Cs = {}# stabilizer check values, these are the measured stabilizer values
    for l in total:
        Cs[tuple(l)] = check_stabilizer(grid, l)
    return Cs

'''constructs the stabilizers for detecting y errors, 
which are the x and z stabilizers along neighboring rows and columns in bs'''
#for scipy decoder
def construct_stabilizers_scipy(d, grid):
    total = []
    for i in range(d-1):
        listrow=[]
        listcol=[]
        for q in range(d):
            listrow.append(d*i +q)
            listrow.append((d)*(i+1) + q)
            listcol.append(d*q +i)
            listcol.append(d*q +(i+1))
        total.append(listrow)
        total.append(listcol) 
    # Cs = {}# stabilizer check values, these are the measured stabilizer values
    I = []#list of all of the stabilizers, which itself is a list that contain the physical qubits in that stabilizer
    C = []#list of syndrome measurement of each of those stabilizers in I
    for l in total:# l is a list of all of the physical qubits in a certain stabilizer 
        I.append(l)
        C.append(check_stabilizer(grid, l))
    return I, C

'''constructs the stabilizers for detecting x errors, 
which are just the z stabilizers in'''
def construct_stabilizers_scipy_x_errors(d, grid):
    total = []
    for i in range(d-1):
        listrow=[]
        for q in range(d):
            listrow.append(d*i +q)
            listrow.append((d)*(i+1) + q)
        total.append(listrow)
    # Cs = {}# stabilizer check values, these are the measured stabilizer values
    I = []#list of all of the stabilizers, which itself is a list that contain the physical qubits in that stabilizer
    C = []#list of syndrome measurement of each of those stabilizers in I
    for l in total:# l is a list of all of the physical qubits in a certain stabilizer 
        I.append(l)
        C.append(check_stabilizer(grid, l))
    return I, C

#for gekko
def solver_to_grid(d, solver_output):
    grid = [[0 for x in range(d)] for y in range(d)] 
    for i in range(d):
        for j in range(d):
            grid[i][j] = int(solver_output[i * d + j][0])
    return grid

#for scipy - changed because scipy output of the guess is different than gekko's
def solver_to_grid_scipy(d, solver_output):
    grid = [[0 for x in range(d)] for y in range(d)] 
    for i in range(d):
        for j in range(d):
            grid[i][j] = solver_output[i * d + j]
    return grid


'''adds two grids using mod 2 addition'''
def add_grids(d, grid1, grid2):
    summed = [[0 for x in range(d)] for y in range(d)] 
    for i in range(d):
        for j in range(d):
            summed[i][j] = (grid1[i][j] + grid2[i][j]) % 2
    return summed


'''
checks is a logical error occurred by "adding" the error grid we created and 
the predicted error grid the MLE solver predicted. There is no logical error
if in the summed grid there is an even # of errors and if all the stabilizers 
are 1
'''
def solver_accuracy(d, grid, predicted):
    #edit this with the ylogical thing
    sum = add_grids(d, grid, predicted)
    num_y_errors = count_y_errors(sum)
    return(num_y_errors % 2 == 0 and check_config(sum))

'''checks to see if the product of the original error grid or '''
def solver_accuracy_x_errors(d, grid, predicted):
    sum = add_grids(d, grid, predicted)
    #check to see if sum is an x logical: an even number of X errors in each row or an odd number of X errors in each row
    errors_per_row = []
    for i in range(d):
        count_per_row = 0
        for j in range(d):
            if sum[i][j] == 1:
                count_per_row += 1
        errors_per_row.append(count_per_row)
    return (all(r1 % 2 == 0 for r1 in errors_per_row)) and check_config_row(sum)


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
