import baconshor
import sys
import math

n = len(sys.argv)
if n != 3:# d and weight
    print("Not enough arguments")
    exit()
d = int(sys.argv[1])
w = int(sys.argv[2])

#figure out how many break up ints of 6e9
breaks = math.ceil(math.comb(d**2, w)/(6e9))
sum = 0
for i in range(breaks):
    sum += baconshor.list_of_grids2(d,w,i)

print(sum)

