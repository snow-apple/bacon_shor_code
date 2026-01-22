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
        print(instruction.targets_copy()[0].value)
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