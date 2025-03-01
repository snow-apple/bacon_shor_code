
from itertools import product
from tabulate import tabulate
import itertools
from itertools import combinations

#false is no why y logical
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
the configuration is possible'''
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

'''Takes in a grid and a list of indexes on the grid and outputs the stabilizer measurement, 1 or -1'''
def check_stabilizer(grid, positions):
    d = len(grid)
    boolean = False

    for p in positions:
        row = (p)//d
        col = (p)%3
        # print(str(row) + ", "+ str(col)+ ": "+str(grid[row][col]))
        boolean = boolean ^ grid[row][col]
    if boolean == False:
        return 1
    else:
        return -1



    

  

'''takes in grid and a list of positions where to place y logicals
and inserts True in those positions'''
def add_y_error(grid,positions):
    d = len(grid)#find length of grid
    for position in positions:
        if type(position) == int:
            row = (position - 1) // d #gives row
            col = (position - 1 )% d #gives col
            # print(row,col)
            grid[row][col] = True

def list_of_grids2(d, weight, printgrid=False):
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
        num = list_of_grids2(d,w, False)
        dict_to_table[count] = [str(w), str(num)]
        count +=1
    print("d="+str(d)+":\n")
    print("{:<10} {:<10}".format('WEIGHT', '# OF COMBINATIONS'))
    for key, value in dict_to_table.items():
        weight, num_of_combinations = value
        print("{:<10} {:<10}".format(weight, num_of_combinations))
    






