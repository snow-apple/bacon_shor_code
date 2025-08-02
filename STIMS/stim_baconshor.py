import numpy as np
import pymatching
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
    

    #Measure X gauges
    circuit += "\n"
    ancilla = d**2
    detector_count = 0
    detector = ""
    for i in range(d):
        detector += f" rec[-{i+1}]"
    for j in range(d-1):
        for i in range(d):
            circuit += f"\nCX {i*d +j} {ancilla}"
            circuit += f"\nCX {i*d +j+1} {ancilla}"
            circuit += f"\nM {ancilla}\n"
            ancilla += 1
        circuit += "\n"
        circuit += f"DETECTOR({detector_count})"
        circuit += detector
        detector_count += 1 
        circuit += "\n"

    #Measure Z gauges
    circuit += "\n"
    circuit += "H" + data_qubits + "\n" #add hadamards on data qubits
    circuit += "H" + measurement_qubits[len(measurement_qubits)//2:] #add hadamards on corresponding measurement qubits
    circuit += "\n"
    
    for j in range(d-1):
        for i in range(d):
            circuit += f"\nCX {ancilla} {i%d +j*d}"
            circuit += f"\nCX {ancilla} {i%d +(j+1)*d}"
            circuit += f"\nH {ancilla}"
            circuit += f"\nM {ancilla}\n"
            ancilla += 1
        circuit += "\n"
        circuit += f"DETECTOR({detector_count})"
        circuit += detector
        detector_count += 1 
        circuit += "\n"
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
        if not np.array_equal(actual_for_shot, predicted_for_shot):
            num_errors += 1
    return num_errors