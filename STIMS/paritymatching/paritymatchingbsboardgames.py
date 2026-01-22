import stim

def split_circuit_into_XZ(original_circuit):
    circuit_X = stim.Circuit()
    circuit_Z = stim.Circuit()
    for instruction in original_circuit:
        if instruction.name != "DETECTOR": #not a detector instruction
            circuit_X.append(instruction)
            circuit_Z.append(instruction)
            continue
        args = instruction.gate_args_copy()
        # print(instruction.targets_copy()[0].value)
        if len(args) >= 4:
            type = args[3]
            if type == 1:
                # Add ONLY to the X-circuit
                circuit_X.append(instruction)
            elif type == 2:
                # Add ONLY to the Z-circuit
                circuit_Z.append(instruction)
            else:#out of precaution
                circuit_X.append(instruction)
                circuit_Z.append(instruction)
        else:
            #out of precaution
            circuit_X.append(instruction)
            circuit_Z.append(instruction)
    return circuit_X, circuit_Z

def edge_coordinate_map(circuit):
    #get coordiantes for every qubit
    qubit_coords = {}
    for instruction in circuit:
        if instruction.name == "QUBIT_COORDS":
            coords = tuple(instruction.gate_args_copy())
            for t in instruction.targets_copy():
                qubit_coords[t.value] = coords
    
    #explains what every single Edge ID actually corresponds to physically in our circuit
    #index = edge_id
    explained_errors = circuit.explain_detector_error_model_errors()
    
    edge_map = {}

    for edge_id, explained_err in enumerate(explained_errors):
        if not explained_err.circuit_error_locations:
            continue
        first_cause = explained_err.circuit_error_locations[0]
        targets = first_cause.instruction_targets.targets_in_range

        #extract location of qubits envolved in this error
        locations = []
        for t in targets:
            if t.coords:
                locations.append(tuple(t.coords))
        edge_map[edge_id] = locations
    return edge_map