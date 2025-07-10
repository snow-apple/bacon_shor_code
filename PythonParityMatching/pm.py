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
    if len(lowest_matching_weights["row"]) == len(lowest_matching_weights["col"]):
        #pair up the row and col list elements to make coordinates to apply the corrections to
        list_of_coords = []
        for i in range(len(lowest_matching_weights["row"])):
            list_of_coords.append((lowest_matching_weights["row"][i], lowest_matching_weights["col"][i]))#adds coordinate tuples
        
        #Using the coordinates, add Y error to the grid
        for coord in list_of_coords:
            predicted_grid[coord[0]][coord[1]] ^= 1 #adds Y error 
    return predicted_grid
    




#generalize code into functions so that I can run in a jupyter notebook

#write code that applies correction based on intersection and then checks
#if the correction was right, using old code or the new technique 

#generate all combos of w = 1 and w = 2 for d = 5, apply this script and check
#if all rows = cols, if so then i can set a condition that if all rows = cols, 
#then apply the intersection correction (check this before #6)
# if not, than still check that if row = col, if applying the intersection works
#both are same the only difference is cehcking if all are row = col,
#for the not case, just keep track of how many are row=col and if they all are correctable using intersection

#if not all are row=col, can they stillbe corrected using intersection broadcasting method?
#if not correctable, is there another method?

#for d = 3,4, are there any that are row = col, or is it always mismatched?
#if always mismatched is it always odd or are there even ones?
# is there any way using the row/col, that pm can correctly correct
#in other words, is the high weight the issue or is it the pattern that's the issue
#and does the high weight cause this pattern? - check this by looking at diff weights for
#diff d values and looking the (d-1)/2 weights vs higher ones. 

#is the intersection/broadcasting technqiue always wrong for the higher weights, cuz
#if it is always wrong than we can correct by applying twice maybe?
