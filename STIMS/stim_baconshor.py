import numpy as np
import pymatching
import stim

'''params: distance d, probabilty of error p, list of positions(starting from 0) to 
place Y errors with probability p
X stabilizers and gauges are vertical along columns
Z stabilizers and gauges are horizontal along rows
constructs the circuit for the BS code with the normal measurement schedule'''
def bacon_shor_circuit(d,p):
    cirq = stim.Circuit()

    # Create the initial qubits - spacial coordinates
    for row in range(d):
        for col in range(d):
            cirq.append("QUBIT_COORDS", d*row + col, (col, row , 0))
            cirq.append("H", d*row + col)

    
    cirq.append("TICK")

    #Measure ZZ checks along rows
    for row in range(d-1):
        for col in range(d):
            cirq.append("MZZ", [d*row + col, d*(row+1) + col]) 
        cirq.append("TICK")
        

    # Measure XX checks along columns
    for col in range(d-1):
        for row in range(d):
            cirq.append("MXX", [d*row + col, d*row + col+1]) 
        cirq.append("TICK")


    # Add Y errors on all qubits with probability p
    for row in range(d):
        for col in range(d):
            cirq.append("Y_ERROR", d*row + col, p)
    # cirq.append("Y_ERROR", 1, p)


    #Measure ZZ checks along rows
    for row in range(d-1):
        for col in range(d):
            cirq.append("MZZ", [d*row + col, d*(row+1) + col]) 
        cirq.append("TICK")

        cirq.append("DETECTOR", [stim.target_rec(-1),stim.target_rec(-2),stim.target_rec(-3),stim.target_rec(-13),stim.target_rec(-14),stim.target_rec(-15)], arg = (col+0.5,d/2,0))

    
    # Measure XX checks along columns
    for col in range(d-1):
        for row in range(d):
            cirq.append("MXX", [d*row + col, d*row + col+1]) 
        cirq.append("TICK")

        #Add detectors for the X checks
        cirq.append("DETECTOR", [stim.target_rec(-1),stim.target_rec(-2),stim.target_rec(-3),stim.target_rec(-13),stim.target_rec(-14),stim.target_rec(-15)], arg = (col+0.5,d/2,0))

    # Add observables for the logical X and Z operators

    # Track logical X along the first row (horizontal)
    for col in range(d):
        cirq.append("OBSERVABLE_INCLUDE", [d*0+col], "X")

    # Track logical Z along the first column (vertical)
    for row in range(d):
        cirq.append("OBSERVABLE_INCLUDE", [d * row + 0], "Z")
    return cirq
   
def run(d, p, shots):
    circuit = bacon_shor_circuit(d, p)
    sampler = circuit.compile_detector_sampler()
    samples = sampler.sample(shots=shots)
    return samples
# print(construct_circuit(3, 0.4, [0]))

def convert_stab_measurements(measurements):
    converted = []
    for i in range(len(measurements)):
        new = []
        for measurement in measurements[i]:
            if measurement == False:
                new.append(1)
            else:
                new.append(-1)
        converted.append(new)
    return converted

# '''gauges is a dictionary with two keys x and z, and each of the values are a list of tuples of what gauges to add '''
# def add_gauges(circuit, gauges):
#     for g in gauges:
#         circuit += g
#     return circuit 

'''from the stim getting_started notebook'''
def count_logical_errors(circuit, num_shots) -> int:
    # Sample the circuit.
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


# #add logical operators to the circuit
# def add_logical_operators(circuit, d):
#     #add logical X operator
#     for i in range(d):
#         circuit += f"\nCX {i} {d**2 + d*(d-1)*2 }"
#     circuit += f"\nM {d**2 + d*(d-1)*2 }\nOBSERVABLE_INCLUDE(0) rec[-1]"
    
#     #add logical Z operator
#     for i in range(d):
#         circuit += f"\nCX {i} {d**2 + d*(d-1)*2 }"
#     circuit += f"\nM {d**2 + d*(d-1)*2 }\nOBSERVABLE_INCLUDE(0) rec[-1]"
    
#     return circuit

