import numpy as np
import pymatching
import stim
'''params: distance d, probabilty of error p, list of positions(starting from 0) to 
place Y errors with probability p
X stabilizers and gauges are vertical along columns
Z stabilizers and gauges are horizontal along rows
constructs the circuit for the BS code with the normal measurement schedule'''
def construct_circuit(d, p, positions):
    circuit = """R"""
    #add data qubits
    data_qubits = ""
    for i in range(d**2):
        data_qubits += f" {i}"
    circuit += data_qubits
    
    #add measurement qubits
    measurement_qubits = ""
    circuit += "\nR"
    for i in range(d*(d-1)*2):
        measurement_qubits += f" {i+d**2}"
    circuit += measurement_qubits

    #add Y errors with prob p
    circuit += "\n"
    circuit += f"\nY_ERROR({p})"
    for index in positions:
        circuit += f" {index}"

    #Measure Z gauges
    circuit += "\n"
    circuit += "\n"
    ancilla = d**2
    detector_count = 0
    detector = ""
    for i in range(d):
        detector += f" rec[-{i+1}]"
    for j in range(d-1):
        for i in range(d):
            circuit += f"\nCX {i%d +j*d} {ancilla}"
            circuit += f"\nCX {i%d +(j+1)*d} {ancilla}"
            circuit += f"\nM {ancilla}\n"
            ancilla += 1
        circuit += "\n"
        circuit += f"DETECTOR({detector_count})"
        circuit += detector
        detector_count += 1 
        circuit += "\n"

    #Measure X gauges
    circuit += "\n"
    
    for j in range(d-1):
        for i in range(d):
            circuit += f"\nH {ancilla}"
            circuit += f"\nCX {ancilla} {i*d +j}"
            circuit += f"\nCX {ancilla} {i*d +j+1}"
            circuit += f"\nH {ancilla}"
            circuit += f"\nM {ancilla}\n"
            ancilla += 1
        circuit += "\n"
        circuit += f"DETECTOR({detector_count})"
        circuit += detector
        detector_count += 1 
        circuit += "\n"
    return circuit

import stim
import numpy as np

def construct_circuit_corrected(d, p):
    circuit = stim.Circuit()

    data_qubits = list(range(d * d))
    ancilla_qubits = list(range(d * d, d * d + 2 * d * (d - 1)))
    
    # Initialize all qubits
    circuit.append("R", data_qubits + ancilla_qubits)
    
    # Add an X error to a specific qubit for testing
    circuit.append("X_ERROR", [1], p=p)

    # Z-gauge measurements
    ancilla_start = d * d
    
    # For each row of Z-stabilizers
    for j in range(d - 1):
        for i in range(d):
            ancilla_qubit = ancilla_start + j * d + i
            circuit.append("H", [ancilla_qubit])
            circuit.append("CZ", [i + j * d, ancilla_qubit])
            circuit.append("CZ", [i + (j + 1) * d, ancilla_qubit])
            circuit.append("H", [ancilla_qubit])
            circuit.append("M", [ancilla_qubit])
            
            # The detector checks the measurement outcome
            # This is where the old code went wrong. We must
            # define the detector immediately after the measurement.
            circuit.append("DETECTOR", [stim.target_rec(-1)])

    # X-gauge measurements
    ancilla_start_x = d * d + d * (d - 1)
    
    for j in range(d - 1):
        for i in range(d):
            ancilla_qubit = ancilla_start_x + j * d + i
            circuit.append("H", [ancilla_qubit])
            circuit.append("CX", [ancilla_qubit, i * d + j])
            circuit.append("CX", [ancilla_qubit, i * d + j + 1])
            circuit.append("H", [ancilla_qubit])
            circuit.append("M", [ancilla_qubit])
            
            # Define detector for this measurement
            circuit.append("DETECTOR", [stim.target_rec(-1)])
            
    # Measure logical operators to determine success
    # This is a key step that was missing in your original code
    circuit.append("M", [0], "observable")

    return circuit
   
def run(d, p, positions, shots):
    circuit = construct_circuit(d, p, positions)
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

def add_qubit_coords(circuit, d):
    coords = ""
    for i in range(d**2):
        coords += f"\nQUBIT_COORDS({i//d}, {i%d}) {i}"
    circuit = coords + "\n" + circuit
    return circuit

def add_ancilla_coords(circuit, d):
    coords = ""
    # Add coordinates for measurement qubits
    for i in range(d*(d-1)):
        coords += f"\nQUBIT_COORDS({i%d}, {i//d + 0.5}) {i + d**2}"
    for i in range(d*(d-1)):
        coords += f"\nQUBIT_COORDS({i//d + 0.5}, {i%d}) {i + d**2 + d*(d-1)}"
    circuit = coords + "\n" + circuit
    return circuit

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

# '''
# CX 0 21
# CX 1 21
# CX 2 21
# CX 3 21
# CX 4 21
# M 21
# OBSERVABLE_INCLUDE(0) rec[-1]

# CX 22 0
# CX 22 5
# CX 22 10
# CX 22 15
# CX 22 20
# H 22
# M 22
# OBSERVABLE_INCLUDE(1) rec[-1]

#  '''



def construct_circuit_corrected(d, p):
    circuit = stim.Circuit()

    data_qubits = list(range(d * d))
    ancilla_qubits = list(range(d * d, d * d + 2 * d * (d - 1)))
    
    # Initialize all qubits
    circuit.append("R", data_qubits + ancilla_qubits)
    
    # Add an X error to a specific qubit for testing
    circuit.append("X_ERROR", [1], p=p)

    # Z-gauge measurements
    ancilla_start = d * d
    
    # For each row of Z-stabilizers
    for j in range(d - 1):
        for i in range(d):
            ancilla_qubit = ancilla_start + j * d + i
            circuit.append("H", [ancilla_qubit])
            circuit.append("CZ", [i + j * d, ancilla_qubit])
            circuit.append("CZ", [i + (j + 1) * d, ancilla_qubit])
            circuit.append("H", [ancilla_qubit])
            circuit.append("M", [ancilla_qubit])
            
            # The detector checks the measurement outcome
            # This is where the old code went wrong. We must
            # define the detector immediately after the measurement.
            circuit.append("DETECTOR", [stim.target_rec(-1)])

    # X-gauge measurements
    ancilla_start_x = d * d + d * (d - 1)
    
    for j in range(d - 1):
        for i in range(d):
            ancilla_qubit = ancilla_start_x + j * d + i
            circuit.append("H", [ancilla_qubit])
            circuit.append("CX", [ancilla_qubit, i * d + j])
            circuit.append("CX", [ancilla_qubit, i * d + j + 1])
            circuit.append("H", [ancilla_qubit])
            circuit.append("M", [ancilla_qubit])
            
            # Define detector for this measurement
            circuit.append("DETECTOR", [stim.target_rec(-1)])
            
    # Measure logical operators to determine success
    # This is a key step that was missing in your original code
    circuit.append("M", [0], "observable")

    return circuit