from baconshor import *

#4. Get Lengths
'''Using the stabilizer measurements store the length of each matching and which rows/cols are 
associated with that matching. I can just create 4 lists, lr1, lr2, lc1, lc2. 1 and 2 are the 
two matching types(two colors), and in the lists ill put which rows/cols have been marked with 
that type. to get the lengths I can just take the len of list'''
#returns the 4 lists
def get_matchings(C):
    row_stab_measurements = C[::2]
    col_stab_measurements = C[1::2]
    r1 = [] # first matching type
    r2 = [] # second matching type
    c1 = [] # first matching type
    c2 = [] # second matching type

    #the first row/col will always be the first matching type
    r1.append(0)
    c1.append(0)
    toggle = 0 # 0 or 1 depending on which matching type/color
    for i,l in enumerate(row_stab_measurements):
        if l == -1:
            toggle ^= 1
        if toggle == 0:
            r1.append(i+1)
        else:
            r2.append(i+1)
        
    toggle = 0# restarting toggle value
    for i,l in enumerate(col_stab_measurements):
        if l == -1:
            toggle ^= 1
        if toggle == 0:
            c1.append(i+1)
        else:
            c2.append(i+1)
    return r1,r2,c1,c2
        
# print("Row Stab measurements: ")
# print(row_stab_measurements)
# print("r1:")
# print(r1)
# print("r2:")
# print(r2)
# print("Col Stab measurements: ")
# print(col_stab_measurements)
# print("c1:")
# print(c1)
# print("c2")


#5. Identify minimum weight rows and cols
#returns a dict of the indices of row and col pair that had the lowest matching weight
def get_lowest_matching(r1,r2,c1,c2):
    lowest_matching_weights = {}
    if len(r1) % 2 == len(c1) % 2:
        #r1 and c1 are a matching and r2 and c2 are a matching
        if len(r1) + len(c1) < len(r2) + len(c2):
            #r1,c1 are the lowest matching pair
            lowest_matching_weights["row"] = r1
            lowest_matching_weights["col"] = c1
        else:
            lowest_matching_weights["row"] = r2
            lowest_matching_weights["col"] = c2
    else:
        #r1 and c2 are a matching and r2 and c1 are a matching
        if len(r1) + len(c2) < len(r2) + len(c1):
            #r1,c2 are the lowest matching pair
            lowest_matching_weights["row"] = r1
            lowest_matching_weights["col"] = c2
        else:
            lowest_matching_weights["row"] = r2
            lowest_matching_weights["col"] = c1

    # print("Rows and Cols associated with the lowest weight matching:")
    # print(lowest_matching_weights)
    return lowest_matching_weights

#6. Applying correction based on intersection - only if row = col
def intersection_correction(d,lowest_matching_weights):
    predicted_grid = create_grid(d)
    
    #pair up the row and col list elements to make coordinates to apply the corrections to
    list_of_coords = []
    for i in range(len(lowest_matching_weights["row"])):
        list_of_coords.append((lowest_matching_weights["row"][i], lowest_matching_weights["col"][i]))#adds coordinate tuples
    
    #Using the coordinates, add Y error to the grid
    for coord in list_of_coords:
        predicted_grid[coord[0]][coord[1]] ^= 1 #adds Y error 
    return predicted_grid
    
#6. Applying correction based on broadcasting - only if row != col
def broadcasting_correction(d,lowest_matching_weights):
    predicted_grid = create_grid(d)

    list_of_coords = []
    if len(lowest_matching_weights["row"]) < len(lowest_matching_weights["col"]):
        if len(lowest_matching_weights["row"]) == 0:
            for i in range(d):
                for j in range(len(lowest_matching_weights["col"])):
                    list_of_coords.append((i, lowest_matching_weights["col"][j]))
        else:
            #row numbers will broadcast out
            for i in range(len(lowest_matching_weights["row"])):
                list_of_coords.append((lowest_matching_weights["row"][i], lowest_matching_weights["col"][i]))#adds coordinate tuples
            for j in range(len(lowest_matching_weights["row"]), len(lowest_matching_weights["col"])):
                list_of_coords.append((lowest_matching_weights["row"][-1], lowest_matching_weights["col"][j]))#adds coordinate tuples

    else:
        if len(lowest_matching_weights["col"]) == 0:
            for j in range(d):
                for i in range(len(lowest_matching_weights["row"])):
                    list_of_coords.append((lowest_matching_weights["row"][i],j))
        else:
            #col numbers will broadcast out
            for i in range(len(lowest_matching_weights["col"])):
                list_of_coords.append((lowest_matching_weights["row"][i], lowest_matching_weights["col"][i]))#adds coordinate tuples
            for j in range(len(lowest_matching_weights["col"]), len(lowest_matching_weights["row"])):
                list_of_coords.append((lowest_matching_weights["row"][j], lowest_matching_weights["col"][-1]))#adds coordinate tuples
    # print(list_of_coords)
    #Using the coordinates, add Y error to the grid
    for coord in list_of_coords:
        predicted_grid[coord[0]][coord[1]] ^= 1 #adds Y error 
    return predicted_grid


#new checking technique