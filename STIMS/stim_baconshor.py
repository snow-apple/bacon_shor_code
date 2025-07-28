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


print(construct_circuit(3, 0.4, [0]))