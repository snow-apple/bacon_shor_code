from baconshor import *

d = 5
error_positions = [1,9]
I = construct_stabilizers_scipy_I(d)
#1. generate array 
grid = create_grid(d)
#2.add errors
add_y_error(grid,error_positions)
print("Error grid:")
Print(grid)
#3. Measure states
C = construct_stabilizers_scipy_C(I,grid)
# print(C)
#4. Get Lengths
'''Using the stabilizer measurements store the length of each matching and which rows/cols are 
associated with that matching. I can just create 4 lists, lr1, lr2, lc1, lc2. 1 and 2 are the 
two matching types(two colors), and in the lists ill put which rows/cols have been marked with 
that type. to get the lengths I can just take the len of list'''
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

print("Rows and Cols associated with the lowest weight matching:")
print(lowest_matching_weights)