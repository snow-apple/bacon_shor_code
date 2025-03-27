import random
import matplotlib.pyplot as plt
#1 means error, 0 means no error

def create_error(d, p):
    error_string = []
    for i in range(d):
        if random.random() < p:
            error_string.append(1)
        else:
            error_string.append(0)
    return error_string


def construct_stabilizers(d, error_string):
    Cs = {}
    numbers = list(range(0, d+1))
    for i in range(d-1):
        
        if (error_string[i]+error_string[i+1]) % 2 == 0:
           Cs[tuple(numbers[i:i+2])] = 1
        else:
           Cs[tuple(numbers[i:i+2])] = -1
    return Cs

def solver_accuracy(d, error_string, predicted):
    count = 0
    for i in range(d):
        if error_string[i] != predicted[i][0]:
            count += 1
    return (count == 0)

def plot(physical, logical):
    fig,ax = plt.subplots(1,1,dpi=200,figsize = (4,3))
    ax.plot(physical,logical)
    ax.legend(fontsize=6)
    ax.set_xlabel("Physical Error Rate (p)")
    ax.set_ylabel("Logical Error Rate")
    plt.plot()