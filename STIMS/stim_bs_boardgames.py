import numpy as np
import pymatching
import stim
import matplotlib.pyplot as plt

'''params: distance d, probabilty of error p, list of positions(starting from 0) to 
place Y errors with probability p
X stabilizers and gauges are vertical along columns
Z stabilizers and gauges are horizontal along rows
constructs the circuit for the BS code with the normal measurement schedule'''
def bacon_shor_measurement_cycle(d):
    cirq = stim.Circuit()

    # Create the initial qubits - spacial coordinates
    for row in range(d):
        for col in range(d):
            cirq.append("QUBIT_COORDS", d*row + col, (col, row , 0))
            # cirq.append("H", d*row + col)
    cirq.append("TICK")


    #0th Step in the Measurement Cycle - X
    for row in range(d):
        cirq.append("MXX", [d*row , d*row +1]) 
   
    cirq.append("MXX", [16,17])
    cirq.append("MXX", [7,8]) 

    for row in range(d):
        cirq.append("MXX", [d*row+3, d*row +3+1]) 
    cirq.append("TICK")

    #1st Step in the Measurement Cycle - Z
    for col in range(d):
        cirq.append("MZZ", [d*0 + col, d*1 + col])
    cirq.append("MZZ", [6,11])
    cirq.append("MZZ", [13,18])
    for col in range(d):
        cirq.append("MZZ", [d*3 + col, d*4 + col])
    cirq.append("TICK")

    #2nd Step in the Measurement Cycle - X
    cirq.append("MXX", [15, 16])
    for row in range(d):
        cirq.append("MXX", [d*row + 1, d*row + 2])
    for row in range(d):
        cirq.append("MXX", [d*row + 2, d*row + 3])
    cirq.append("MXX", [8, 9])
    cirq.append("TICK")

    #3rd Step in the Measurement Cycle - Z
    cirq.append("MZZ", [1,6])
    for col in range(d):
        cirq.append("MZZ", [d*1 + col, d*2 + col])
    for col in range(d):
        cirq.append("MZZ", [d*2 + col, d*3 + col])
    cirq.append("MZZ", [18,23])
    cirq.append("TICK")
    
    return cirq
   
def generate_detector_gauges(d):
    gauges = []

    if d == 5:
        # 3 first 
        # 4 first 
        gauges.append()


    #X Gauges
    for row in range(d):
        for col in range(d-1):
            gauges.append(([d*row + col, d*row + col+1], 'X'))
    #Z Gauges
    for col in range(d):
        for row in range(d-1):
            gauges.append(([d*row + col, d*(row+1) + col], 'Z'))
    return gauges


#when creating grids > d = 5. combine the circuits and remove gauges from measurement schedule after?





def bacon_shor_five_initialization(d):
    cirq = stim.Circuit()

    # Create the initial qubits - spacial coordinates
    num_data_qubits = d * d
    for row in range(d):
        for col in range(d):
            cirq.append("QUBIT_COORDS", d*row + col, (col, row , 0))
            cirq.append("H", d*row + col)
    cirq.append("TICK")

    #----------------------------------------------------------------
    #INITIALIZATION CYCLE - START MEASURING GAUGES
    #----------------------------------------------------------------

    #0th Step in the Measurement Cycle - X
    for row in range(d):
        cirq.append("MXX", [d*row , d*row +1]) 
   
    cirq.append("MXX", [16,17])
    cirq.append("MXX", [7,8]) 

    for row in range(d):
        cirq.append("MXX", [d*row+3, d*row +3+1]) 
    # cirq.append("DETECTOR", [stim.target_rec(-1)]) 
    cirq.append("TICK")

    

    #1st Step in the Measurement Cycle - Z
    for col in range(d):
        cirq.append("MZZ", [d*0 + col, d*1 + col])
    cirq.append("MZZ", [6,11])
    cirq.append("MZZ", [13,18])
    for col in range(d):
        cirq.append("MZZ", [d*3 + col, d*4 + col])
    cirq.append("TICK")

    #2nd Step in the Measurement Cycle - X
    cirq.append("MXX", [15, 16])
    for row in range(d):
        cirq.append("MXX", [d*row + 1, d*row + 2])
    for row in range(d):
        cirq.append("MXX", [d*row + 2, d*row + 3])
    cirq.append("MXX", [8, 9])
    cirq.append("TICK")

    #3rd Step in the Measurement Cycle - Z
    cirq.append("MZZ", [1,6])
    for col in range(d):
        cirq.append("MZZ", [d*1 + col, d*2 + col])
    for col in range(d):
        cirq.append("MZZ", [d*2 + col, d*3 + col])
    cirq.append("MZZ", [18,23])
    cirq.append("TICK")
    return cirq

def bacon_shor_five_measurements(d,cirq,p, add_errors = False):
    #added errors
    #----------------------------------------------------------------
    #MEASUREMENT CYCLE REPEATS - START MEASURING DETECTORS
    #----------------------------------------------------------------
    
     #4th Step in the Measurement Cycle - X
    for row in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*row,d*row+1], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MXX", [d*row , d*row +1]) 

    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [16,17], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MXX", [16,17])

    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [7,8], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MXX", [7,8]) 

    for row in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*row+3,d*row+4], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MXX", [d*row+3, d*row +3+1]) 
    cirq.append("TICK")

    #5th Step in the Measurement Cycle - Z
    for col in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*0 + col,d*1 + col], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MZZ", [d*0 + col, d*1 + col])

    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [6,11], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MZZ", [6,11])

    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [13,18], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MZZ", [13,18])

    for col in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*3 + col,d*4 + col], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MZZ", [d*3 + col, d*4 + col])
    cirq.append("TICK")

    #6th Step in the Measurement Cycle - X
    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [15,16], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MXX", [15, 16])
    for row in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*row + 1,d*row + 2], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MXX", [d*row + 1, d*row + 2])
    for row in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*row + 2,d*row + 3], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MXX", [d*row + 2, d*row + 3])

    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [8,9], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MXX", [8, 9])
    cirq.append("TICK")

    #7th Step in the Measurement Cycle - Z
    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [1,6], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MZZ", [1,6])
    for col in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*1 + col,d*2 + col], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MZZ", [d*1 + col, d*2 + col])
    for col in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*2 + col,d*3 + col], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MZZ", [d*2 + col, d*3 + col])

    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [18,23], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MZZ", [18,23])
    cirq.append("TICK")


    #4th Step in the Measurement Cycle - X
    for row in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*row,d*row +1], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MXX", [d*row , d*row +1]) 
    
    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [16,17], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MXX", [16,17])
    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [7,8], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MXX", [7,8]) 

    for row in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*row+3,d*row+4], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MXX", [d*row+3, d*row +3+1]) 
    cirq.append("TICK")

    #5th Step in the Measurement Cycle - Z
    for col in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*0 + col,d*1 + col], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MZZ", [d*0 + col, d*1 + col])

    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [6,11], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MZZ", [6,11])
    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [13,18], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MZZ", [13,18])
    for col in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*3 + col,d*4 + col], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MZZ", [d*3 + col, d*4 + col])
    cirq.append("TICK")

    #6th Step in the Measurement Cycle - X
    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [15,16], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MXX", [15, 16])
    for row in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*row + 1,d*row + 2], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MXX", [d*row + 1, d*row + 2])
    for row in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*row + 2,d*row + 3], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MXX", [d*row + 2, d*row + 3])

    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [8,9], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MXX", [8, 9])
    cirq.append("TICK")

    #7th Step in the Measurement Cycle - Z
    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [1,6], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MZZ", [1,6])
    for col in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*1 + col,d*2 + col], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MZZ", [d*1 + col, d*2 + col])
    for col in range(d):
        inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [d*2 + col,d*3 + col], gate_args = [p])
        cirq.append(inst) if add_errors else None
        cirq.append("MZZ", [d*2 + col, d*3 + col])

    inst = stim.CircuitInstruction(name = "DEPOLARIZE1", targets = [18,23], gate_args = [p])
    cirq.append(inst) if add_errors else None
    cirq.append("MZZ", [18,23])
    cirq.append("TICK")


    return cirq


def bacon_shor_detectors():
    detectors = []
    #x detectors 
    detectors.append([-96,-95,-94,-72,-48,-47,-46,-45])
    detectors.append([-93,-92,-72,-44])
    detectors.append([-71,-70,-69,-68,-43,-23,-22,-21])
    detectors.append([-67,-43,-20,-19])
    detectors.append([-66,-42,-18,-17])
    detectors.append([-65,-64,-63,-62,-42,-16,-15,-14])
    detectors.append([-89,-88,-61,-41])
    detectors.append([-87,-86,-85,-61,-40,-39,-38,-37])

    #z detectors]

    detectors.append([-83,-82,-81,-80,-60,-34,-33,-32])
    detectors.append([-84,-60,-36,-35])
    detectors.append([-57,-56,-55,-31,-10,-9,-8,-7])
    detectors.append([-59,-58,-31,-11])
    detectors.append([-51,-50,-30,-2])
    detectors.append([-54,-53,-52,-30,-6,-5,-4,-3])

    detectors.append([-73,-49,-26,-25])
    detectors.append([-77,-76,-75,-74,-49,-29,-28,-27])

    return detectors

def final_round_detectors():
    #use same detectors as before but account for the shift in 25 of the measured qubits at the end of the circuit
    detectors = []
    #x detectors 
    detectors.append([-48-25,-47-25,-46-25,-24-25,-25,-24,-20,-19,-15,-14,-10,-9])
    detectors.append([-45-25,-44-25,-24-25,-5,-4])
    detectors.append([-23-25,-22-25,-21-25,-20-25,-24,-23,-19,-18,-14,-13,-9,-8])
    detectors.append([-19-25,-4,-3])
    detectors.append([-18-25,-23,-22])
    detectors.append([-17-25,-16-25,-15-25,-14-25,-18,-17,-13,-12,-8,-7,-3,-2])
    detectors.append([-41-25,-40-25,-13-25,-22,-21])
    detectors.append([-39-25,-38-25,-37-25,-13-25,-17,-16,-12,-11,-7,-6,-2,-1])

    # #z detectors

    # detectors.append([-83-25,-82-25,-81-25,-80-25,-60-25,-34-25,-33-25,-32-25,-24,-19,-23,-18,-22,-17,-21,-16])
    # detectors.append([-84-25,-60-25,-36-25,-35-25,-25,-20,-24,-19])
    # detectors.append([-57-25,-56-25,-55-25,-31-25,-10-25,-9-25,-8-25,-7-25,-18,-13,-17,-12,-16,-11])
    # detectors.append([-59-25,-58-25,-31-25,-11-25,-20,-15,-19,-14])

    # detectors.append([-51-25,-50-25,-30-25,-2-25,-12,-7,-11,-6])
    # detectors.append([-54-25,-53-25,-52-25,-30-25,-6-25,-5-25,-4-25,-3-25,-15,-10,-14,-9,-13,-8])
    # detectors.append([-73-25,-49-25,-26-25,-25-25,-7,-2,-6,-1])
    # detectors.append([-77-25,-76-25,-75-25,-74-25,-49-25,-29-25,-28-25,-27-25,-10,-5,-9,-4,-8,-3,-7,-2])
    return detectors



def bacon_shor_observables(d,circuit):
    all_qubits = range(d * d)
    circuit.append("MX", all_qubits)

    obs_targets = []
    for row in range(d):
        qubit_index = row * d  # 0, 5, 10...
        
        # Convert qubit index to record offset
        # Offset = qubit_index - total_num_qubits
        offset = qubit_index - (d * d)
        
        obs_targets.append(stim.target_rec(offset))

    # 3. DEFINE THE OBSERVABLE
    circuit.append("OBSERVABLE_INCLUDE", obs_targets, 0)

    # Logical X: measured along a row (horizontal)
    # Logical Z: measured along a column (vertical)

    # Logical X observable - measure Z along first column
    # for row in range(d):
    #     circuit.append("MX", [d*row + 0])
    # obs_z = [stim.target_rec(-(i+1)) for i in range(d)]
    # circuit.append("OBSERVABLE_INCLUDE", obs_z, 0)

    # # Logical Z observable - measure X along first row
    # for col in range(d):
    #     circuit.append("MZ", [d*0 + col])
    # obs_x = [stim.target_rec(-(i+1)) for i in range(d)]
    # circuit.append("OBSERVABLE_INCLUDE", obs_x, 1)
    return circuit

def bacon_shor_apply_detector(detectors,cirq):
    cirq.append("DETECTOR", [stim.target_rec(i) for i in detectors])
    return cirq


def bacon_shor_circuit(d,p,rounds, add_Errors = False):
    cirq = bacon_shor_five_initialization(d)

    detectors = bacon_shor_detectors()

    for _ in range(rounds):

        cirq = bacon_shor_five_measurements(d,cirq,p,add_Errors)
        for det in detectors:
        # cirq = bacon_shor_five_measurements(d,cirq)
            cirq = bacon_shor_apply_detector(det,cirq)
    cirq = bacon_shor_observables(d,cirq)

    final_detectors = final_round_detectors()
    for det in final_detectors:
        cirq = bacon_shor_apply_detector(det,cirq)
    # num = count_logical_errors(cirq,10)
    # print(num)
    
    return cirq



def count_logical_errors(circuit, num_shots) -> int:

    sampler = circuit.compile_detector_sampler()
    detection_events, observable_flips = sampler.sample(num_shots, separate_observables=True)
    print("detection events", detection_events)
    print("observable flips", observable_flips)

    # Configure a decoder using the circuit.
    detector_error_model = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(detector_error_model)

    # Run the decoder.
    predictions = matcher.decode_batch(detection_events)

    # Count the mistakes.
    num_errors = 0
    for shot in range(num_shots):
        actual_for_shot = observable_flips[shot]
        predicted_for_shot = predictions[shot]
        print(f"Shot {shot}: actual={actual_for_shot}, predicted={predicted_for_shot}")
        # If the actual and predicted observable flips are not equal, count it as an error.
        if not np.array_equal(actual_for_shot, predicted_for_shot):
            num_errors += 1
    return num_errors

def plot_threshold(d=5, ps=None, num_shots=1000):
    if ps is None:
        ps = np.linspace(0.001, 0.1, 10)
    logical_error_rates = []
    logical_error_stds = []

    for p in ps:
        print(f"\n=== Running d={d}, p={p:.5f} ===")
        circuit = bacon_shor_circuit(d, p, add_Errors=True)
        num_logical_errors = count_logical_errors(circuit, num_shots)
        logical_error_rate = num_logical_errors / num_shots
        std = np.sqrt(logical_error_rate * (1 - logical_error_rate) / num_shots)
        logical_error_rates.append(logical_error_rate)
        logical_error_stds.append(std)
        print(f"Logical error rate at p={p:.5f}: {logical_error_rate:.4f}")

    plt.figure(figsize=(8, 6))
    plt.errorbar(ps, logical_error_rates, yerr=logical_error_stds, fmt='o-', capsize=4, label=f'd={d}')
    # plt.xscale('log')
    # plt.yscale('log')
    plt.xlabel("Physical error rate p")
    plt.ylabel("Logical error rate p_L")
    plt.title("Bacon–Shor Logical Error Rate vs Physical Error Rate")
    plt.grid(True, which="both")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_low_p(d=5, ps=None, num_shots=1000):
    if ps is None:
        ps = np.linspace(0.00001, 0.01, 10)
    logical_error_rates = []
    logical_error_stds = []

    for p in ps:
        print(f"\n=== Running d={d}, p={p:.5f} ===")
        circuit = bacon_shor_circuit(d, p, add_Errors=True)
        num_logical_errors = count_logical_errors(circuit, num_shots)
        logical_error_rate = num_logical_errors / num_shots
        std = np.sqrt(logical_error_rate * (1 - logical_error_rate) / num_shots)
        logical_error_rates.append(logical_error_rate)
        logical_error_stds.append(std)

        print(f"Logical error rate at p={p:.5f}: {logical_error_rate:.4f}")

    p_last = ps[-1]
    pl_last = logical_error_rates[-1]
    
    # Calculate the slope 'm' of a line from (0,0) to the last point.
    if p_last == 0:
        m_slope = 0
    else:
        m_slope = pl_last / p_last  # m = (y2 - y1) / (x2 - x1) = (pl_last - 0) / (p_last - 0)

    # Create the y_fit list using this new slope 'm'
    y_fit = [m_slope * p for p in ps]
    fit_label = f'Fit from last point: y = {m_slope:.4f}x'


    plt.figure(figsize=(8, 6))
    plt.errorbar(ps, logical_error_rates, yerr=logical_error_stds, fmt='o-', capsize=4, label=f'd={d}')
    plt.plot(ps, y_fit, label=fit_label, color='red', linestyle='--')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Physical error rate p")
    plt.ylabel("Logical error rate p_L")

    plt.title("Bacon–Shor Logical Error Rate vs Physical Error Rate")
    plt.grid(True, which="both")
    plt.legend()
    plt.tight_layout()
    plt.show()
# #use the noise model from stim_baconshor.py to add errors




#TO DOs:
#put measurement noise - decode using pymatching for x/z
#convert measurement scheduole into a programmatic form
#genealize for higher d




#To Dos: 10/22
#get sinter to work
#build rep code and look at slope for that - DONE
#what should slope be for rep code? - realted to P_L equation - DONE
# same for bacon shor?


#plot for low p - up to 10^-5 
#What should the slope be?

#why plot platueing at the end?



#