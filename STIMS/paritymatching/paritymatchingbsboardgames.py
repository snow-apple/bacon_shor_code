import stim
import pymatching
import numpy as np

# def split_circuit_into_XZ(original_circuit):
#     circuit_X = stim.Circuit()
#     circuit_Z = stim.Circuit()
#     for instruction in original_circuit:
#         if instruction.name != "DETECTOR": #not a detector instruction
#             circuit_X.append(instruction)
#             circuit_Z.append(instruction)
#             continue
#         args = instruction.gate_args_copy()
#         # print(instruction.targets_copy()[0].value)
#         if len(args) >= 4:
#             type = args[3]
#             if type == 1:
#                 # Add ONLY to the X-circuit
#                 circuit_X.append(instruction)
#             elif type == 2:
#                 # Add ONLY to the Z-circuit
#                 circuit_Z.append(instruction)
#             else:#out of precaution
#                 circuit_X.append(instruction)
#                 circuit_Z.append(instruction)
#         else:
#             #out of precaution
#             circuit_X.append(instruction)
#             circuit_Z.append(instruction)
#     return circuit_X, circuit_Z

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

'''returns edges found for X and Z errors separately'''
def matching(circuit):
    dem = circuit.detector_error_model(decompose_errors=True)
    full_matcher = pymatching.Matching.from_detector_error_model(dem)

    x_det_indices = [] # Detectors that check for Z-errors
    z_det_indices = [] # Detectors that check for X-errors
    det_coords = circuit.get_detector_coordinates()
    for index, coords in det_coords.items():
        if len(coords) >= 4:
            check = coords[3]
            if check == 1.0:
                x_det_indices.append(index)
            elif check == 2.0:
                z_det_indices.append(index)

    sampler = circuit.compile_detector_sampler()
    shot = sampler.sample(1)[0].flatten().astype(np.uint8)

    #find z errors using x detectors and get the edges
    x_shot = shot.copy()
    x_shot[z_det_indices] = 0  #set the z detectors to 0
    edges_X = full_matcher.decode_to_edges_array(x_shot)

    #find x errors using z detectors and get the edges
    z_shot = shot.copy()
    z_shot[x_det_indices] = 0  #set the x detectors to
    edges_Z = full_matcher.decode_to_edges_array(z_shot)

    return edges_X, edges_Z

'''returns the physical locations of the errors from the edges found'''
def get_locations_from_edges(circuit, edges_X, edges_Z):
    full_map = edge_coordinate_map(circuit)

    #extract location of z errors on x circuit
    z_error_locations = []
    if isinstance(edges_X, np.ndarray):
        edges_X = edges_X.flatten()
    for edge_id in edges_X:
        if edge_id == -1: continue
        if edge_id in full_map:
            z_error_locations.extend(full_map[edge_id])

    #extract location of x errors on z circuit
    x_error_locations = []
    if isinstance(edges_Z, np.ndarray):
        edges_Z = edges_Z.flatten()
    for edge_id in edges_Z:
        if edge_id == -1: continue
        if edge_id in full_map:
            x_error_locations.extend(full_map[edge_id])
    return z_error_locations, x_error_locations

def intersection(z_error_locations, x_error_locations):
    #remove duplciates
    set_z_errors = set(z_error_locations)
    set_x_errors = set(x_error_locations)

    y_errors = set_z_errors.intersection(set_x_errors)

    print(f"Found {len(y_errors)} Y-Errors at: {y_errors}")
    return y_errors