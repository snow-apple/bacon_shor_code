from random import random

import stim
import pymatching
import numpy as np

from stim_baconshor import bacon_shor_circuit_manual_errors

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
    # print(f"Qubit coordinates: {qubit_coords}")
    
    #explains what every single Edge ID actually corresponds to physically in our circuit
    #index = edge_id
    explained_errors = circuit.explain_detector_error_model_errors()
    # print(f"Explained errors: {explained_errors}")    
    edge_map = {}

    for edge_id, explained_err in enumerate(explained_errors):
        if not explained_err.circuit_error_locations:
            continue
        first_cause = explained_err.circuit_error_locations[0]
        targets = first_cause.instruction_targets.targets_in_range
        # print(f"Edge ID {edge_id} corresponds to targets: {targets}")

        #extract location of qubits envolved in this error
        locations = []
        for t in targets:
            if t.coords:
                locations.append(tuple(t.coords))
        edge_map[edge_id] = locations
    return edge_map

# '''returns edges found for X and Z errors separately'''
# def matching(circuit):
#     dem = circuit.detector_error_model(decompose_errors=True)
#     full_matcher = pymatching.Matching.from_detector_error_model(dem)

#     x_det_indices = [] # Detectors that check for Z-errors
#     z_det_indices = [] # Detectors that check for X-errors
#     det_coords = circuit.get_detector_coordinates()
#     for index, coords in det_coords.items():
#         if len(coords) >= 4:
#             check = coords[3]
#             if check == 1.0:
#                 x_det_indices.append(index)
#             elif check == 2.0:
#                 z_det_indices.append(index)

#     sampler = circuit.compile_detector_sampler()
#     shot = sampler.sample(1)[0].flatten().astype(np.uint8)

#     #find z errors using x detectors and get the edges
#     x_shot = shot.copy()
#     x_shot[z_det_indices] = 0  #set the z detectors to 0
#     edges_X = full_matcher.decode_to_edges_array(x_shot)

#     #find x errors using z detectors and get the edges
#     z_shot = shot.copy()
#     z_shot[x_det_indices] = 0  #set the x detectors to
#     edges_Z = full_matcher.decode_to_edges_array(z_shot)

#     return edges_X, edges_Z
'''returns edges found for X and Z errors separately'''
def matching(circuit):
    dem = circuit.detector_error_model(decompose_errors=True)
    full_matcher = pymatching.Matching.from_detector_error_model(dem)

    # Force Weights to 1.0 so we don't exceed the 16777215 limit
    #By default, PyMatching gives higher weights to rare errors. 
    # overriding this so every qubit error has a weight of exactly 1.0
    num_detectors = full_matcher.num_detectors
    for u, v, data in full_matcher.edges():
        u_node = u if u is not None else num_detectors
        v_node = v if v is not None else num_detectors
        full_matcher.add_edge(u_node, v_node, weight=1.0, 
                             fault_ids=data.get('fault_ids', set()), 
                             merge_strategy="replace")
        
    det_coords = circuit.get_detector_coordinates()
    x_det_indices = [i for i, c in det_coords.items() if len(c) >= 4 and c[3] == 1.0]# Detectors that check for Z-errors
    z_det_indices = [i for i, c in det_coords.items() if len(c) >= 4 and c[3] == 2.0]# Detectors that check for X-errors

    #runs the quantum simulation for one shot.
    #  It checks which detectors actually flipped
    sampler = circuit.compile_detector_sampler()
    shot = sampler.sample(1)[0] 

    #  FIND EDGES FOR X 
    # INSTEAD OF np.zeros(num_detectors), use the matcher's own required shape
    actual_required_shape = full_matcher.num_detectors
    
    x_shot = np.zeros(actual_required_shape, dtype=np.uint8)
    # Only fill indices that exist in BOTH our list and the actual shot
    for i in x_det_indices:
        if i < len(shot):
            x_shot[i] = shot[i]
    #PyMatching looks at all the lit detectors in x_shotand 
    #  tries to pair them up or connect them to the boundary using the fewest number of 
    # edges possible.
    # returns an array of Edge IDs  
    # These edges represent the specific qubits the decoder blames for the syndrome.
    edges_X = full_matcher.decode_to_edges_array(x_shot)

    # FIND EDGES FOR Z 
    z_shot = np.zeros(actual_required_shape, dtype=np.uint8)
    for i in z_det_indices:
        if i < len(shot):
            z_shot[i] = shot[i]
            
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

#--Functions for Parity Matching with Pymatching Static Schedule--
'''returns the weight of the solution found by PyMatching and the weight of the alternate solution, 
as well as what the alternate solution actually is'''
def get_all_solutions(d, x_edges, z_edges):
    weight_py_solution_x = len(z_edges)
    # print(f"Weight of PyMatching solution on X graph: {weight_py_solution_x}")
    weight_py_solution_z = len(x_edges)
    # print(f"Weight of PyMatching solution on Z graph: {weight_py_solution_z}")
    weight_alternate_solution_x = d - weight_py_solution_x
    weight_alternate_solution_z = d - weight_py_solution_z

    current_x = [set(edge) for edge in z_edges]
    current_z = [set(edge) for edge in x_edges]
    # print(f"Current X graph: {current_x}")
    # print(f"Current Z graph: {current_z}")

    #create set with all possible edges on Z graph
    all_z_edges = []
    for i in range(d-2):
        all_z_edges.append({i, i+1})
    all_z_edges.append({-1, 0}) #add boundary edge
    all_z_edges.append({-1, d-2}) #add boundary edge
    # print(f"All possible edges on Z graph: {all_z_edges}")

    #create set with all possible edges on X graph
    all_x_edges = []
    for i in range(d-1, 2*d-3):
        all_x_edges.append({i, i+1})
    all_x_edges.append({-1, d-1}) #add boundary edge
    all_x_edges.append({-1, 2*d-3}) #add boundary edge

    alternate_x_solution = [edge for edge in all_x_edges if edge not in current_x]
    alternate_z_solution = [edge for edge in all_z_edges if edge not in current_z]

    dict_X = {}
    dict_X[weight_py_solution_x] = current_x
    dict_X[weight_alternate_solution_x] = alternate_x_solution
    dict_Z = {}
    dict_Z[weight_py_solution_z] = current_z
    dict_Z[weight_alternate_solution_z] = alternate_z_solution

    return dict_X, dict_Z

def choose_lowest_weight_parity(dict_X, dict_Z):
    even_x = sum(w for w in dict_X if w % 2 == 0)
    odd_x  = sum(w for w in dict_X if w % 2 != 0)

    even_z = sum(w for w in dict_Z if w % 2 == 0)
    odd_z  = sum(w for w in dict_Z if w % 2 != 0)
    
    even_solution = even_x + even_z
    odd_solution = odd_x + odd_z

    if even_solution < odd_solution:
        # print(f"Choosing even solution with weight {even_x}, {even_z}")
        return dict_X[even_x], dict_Z[even_z]
    else: #odd_solution < even_solution:
        # print(f"Choosing odd solution with weight {odd_x}, {odd_z}")
        return dict_X[odd_x], dict_Z[odd_z]
    
'''check if the solution found by PyMatching is correct by seeing if the edges
     it found correspond to the actual error locations, the intersection
     y error locations: a list of where Y errors are located'''
def did_pass(d, x_graph_solution, z_graph_solution, y_error_locations):
    #get the rows and columns of the original y error locations 
    #the rows correspond to the Z graph and the columns correspond to the X graph
    y_rows = set()
    y_cols = set()
    for location in y_error_locations:
        y_rows.add(location // d)
        y_cols.add(location % d)
    # print(f"Y errors are located in rows {y_rows} and columns {y_cols}")

    x_edges_dict, z_edges_dict = map_edges_to_rowcol(d)
    x_graph_locations = set()
    for edge in x_graph_solution:
        if edge in x_edges_dict.values():
            keys = [k for k, v in x_edges_dict.items() if v == edge]
            x_graph_locations.add(keys[0]) #there should only be one key that corresponds to this edge, but we have to put it in a list to get it out of the dictionary
    
    z_graph_locations = set()
    for edge in z_graph_solution:
        if edge in z_edges_dict.values():
            keys = [k for k, v in z_edges_dict.items() if v == edge]
            z_graph_locations.add(keys[0]) #there should only be one key that corresponds to this edge, but we have to put it in a list to get it out of the dictionary
    
    # print("Z graph solution corresponds to rows: ", z_graph_locations)
    # print("X graph solution corresponds to columns: ", x_graph_locations)

    if z_graph_locations == y_rows and x_graph_locations == y_cols:
        # print("PASS: ParityMatching solution is correct!")
        return True
    else:        
        # print("FAIL: ParityMatching solution is incorrect.")
        return False

    

    


'''map the edges found to the row and column they correspond to in the Bacon-Shor code'''
def map_edges_to_rowcol(d):
    ##create set with all possible edges on Z graph
    #create set with all possible edges on Z graph
    z_edges_dict = {}
    for i in range(d-2):
        z_edges_dict[i+1] = {i, i+1}
    z_edges_dict[0] = {-1, 0} #add boundary edge
    z_edges_dict[d-1] = {-1, d-2} #add boundary edge
    # print(f"All possible edges on Z graph: {z_edges_dict}")

    #create set with all possible edges on X graph
    x_edges_dict = {}
    for i in range(d-1, 2*d-3):
        x_edges_dict[i-d+2] = {i, i+1}
    x_edges_dict[0] = {-1, d-1} #add boundary edge
    x_edges_dict[d-1] = {-1, 2*d-3} #add boundary edge
    # print(f"All possible edges on X graph: {x_edges_dict}")
    return x_edges_dict, z_edges_dict

# '''map the edges found to the row and column they correspond to in the Bacon-Shor code'''
# def map_rowcol_to_edges(d):

#     #create set with all possible edges on Z graph
#     z_edges_dict = {}
#     for i in range(d - 2):
#         z_edges_dict[frozenset({i, i + 1})] = i + 1
#     z_edges_dict[frozenset({-1, 0})] = 0
#     z_edges_dict[frozenset({-1, d - 2})] = d - 1

#     # create set with all possible edges on X graph
#     x_edges_dict = {}
#     for i in range(d - 1, 2 * d - 3):
#         x_edges_dict[frozenset({i, i + 1})] = i - d + 2
#     x_edges_dict[frozenset({-1, d - 1})] = 0
#     x_edges_dict[frozenset({-1, 2 * d - 3})] = d - 1
    
#     return x_edges_dict, z_edges_dict


def run(d, error_positions):
    circuit = bacon_shor_circuit_manual_errors(d=d, error_positions=error_positions)
    x_edges, z_edges= matching(circuit)
    dict_X, dixt_Z = get_all_solutions(d, x_edges, z_edges)
    x_graph_solution, z_graph_solution = choose_lowest_weight_parity(dict_X, dixt_Z)
    outcome = did_pass(d, x_graph_solution, z_graph_solution, error_positions)
    return outcome

"""Returns a list of qubit indices that suffered an error based on probability p."""
def generate_random_errors(d, p):
    # This creates an array of d^2 random numbers and returns the indices where they are < p
    probs = np.random.rand(d**2)
    errors = np.where(probs < p)[0].tolist()
    return errors

def get_logical_error_rate(d, p, num_shots=10):
    logical_errors = 0
    for _ in range(num_shots):
        error_positions = generate_random_errors(d, p)
        # We simulate the circuit and run parity matching pipeline
        if not run(d, error_positions):
            logical_errors += 1
    
    return logical_errors / num_shots
