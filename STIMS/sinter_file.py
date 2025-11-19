import stim
import sinter
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing
import time
from stim_bs_boardgames import bacon_shor_circuit


def run_sinter_simulation_rep_code( distances, p_values, num_rounds,print_progress=True):
    tasks = []
    for d in distances:
        for p in p_values:
            circuit = stim.Circuit.generated(
            "repetition_code:memory",
            distance=d,
            rounds=num_rounds,
            after_clifford_depolarization=p  # 1% noise
        )

            tasks.append(sinter.Task(
                            circuit=circuit,
                            json_metadata={
                                'd': d,
                                'p': p,
                                'rounds': num_rounds,
                            }
                        ))
    if print_progress:
        print(f"Generated {len(tasks)} tasks.")
        print("--- Starting sinter.collect ---")

    start_time = time.time()

    collected_samples: list[sinter.AnonTaskStats()] = sinter.collect(
        # Use all available CPU cores for max speed
        num_workers=multiprocessing.cpu_count(),
        tasks=tasks,
        decoders=['pymatching'],
        max_errors=500,        # This is the "target errors"
        max_shots=10_000_000,  # Safety cap for very-low-noise
        print_progress=True,
    )
    end_time = time.time()

    if print_progress:
        print(f"\n--- Sinter finished successfully in {end_time - start_time:.2f}s ---")

    return collected_samples

def sinter_plot(collected_samples, d, title, errorbars = False):
    plot_data_by_distance = {}
    if errorbars:
        for sample in collected_samples:
            d = sample.json_metadata['d']
            p = sample.json_metadata['p']
            log_error_prob = sample.errors / sample.shots#gets error rate
            std = np.sqrt((log_error_prob * (1-log_error_prob))/sample.shots) # standard deviation
    
            if d not in plot_data_by_distance:
                plot_data_by_distance[d] = {
                    'p_values': [],
                    'pl_values': [],
                    'std_errors': []
            }
            
            plot_data_by_distance[d]['p_values'].append(p)
            plot_data_by_distance[d]['pl_values'].append(log_error_prob)
            plot_data_by_distance[d]['std_errors'].append(std)


        plt.figure(figsize=(8, 6))

        for d, data in plot_data_by_distance.items():
            #sort p avlues
            sorter = np.argsort(data['p_values']) #gives the indices that sort the list
            x = np.array(data['p_values'])[sorter]
            y = np.array(data['pl_values'])[sorter]
            y_err = np.array(data['std_errors'])[sorter]

            fit_indices = np.where(x < 0.01)
            x_fit = x[fit_indices]
            y_fit = y[fit_indices]
            if len(x_fit) > 1:
                # 3. Convert to log-space
                log_x = np.log10(x_fit)
                log_y = np.log10(y_fit)
                
                # 4. Perform the 1st-degree (linear) fit
                #    coeffs[0] is the slope (k), coeffs[1] is the intercept
                coeffs = np.polyfit(log_x, log_y, 1)
                slope = coeffs[0]
                intercept = coeffs[1]
                
                # Print the measured slope
                expected_k = np.ceil(d / 2)
                print(f"d={d}: Measured Slope k = {slope:.4f} (Expected: {expected_k})")
                
                # 5. Create the fitted line data for plotting
                #    (Use all x_data to draw the line across the whole plot)
                y_fit_line = 10**(slope * np.log10(x) + intercept)
                
                # 6. Plot the fitted line
                plt.plot(x, y_fit_line, '--', label=f"Fit $d={d}$ (slope={slope:.2f})")


            plt.errorbar( x,y, yerr=y_err, fmt='o-',capsize=5,label=f"Distance $d={d}$" )
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel("Physical Error Rate ($p$)")
        plt.ylabel("Logical Error Rate ($P_L$)")
        plt.title(f"{title} Logical Error Rate vs. Physical Error Rate")
        plt.grid(True, which="both", ls="--")
        plt.legend()
        plt.show()
    else:
        for sample in collected_samples:
            d = sample.json_metadata['d']
            p = sample.json_metadata['p']
            log_error_prob = sample.errors / sample.shots#gets error rate
    
            if d not in plot_data_by_distance:
                plot_data_by_distance[d] = {
                    'p_values': [],
                    'pl_values': [],
            }
            
            plot_data_by_distance[d]['p_values'].append(p)
            plot_data_by_distance[d]['pl_values'].append(log_error_prob)


        plt.figure(figsize=(8, 6))

        for d, data in plot_data_by_distance.items():
            #sort p avlues
            sorter = np.argsort(data['p_values']) #gives the indices that sort the list
            x = np.array(data['p_values'])[sorter]
            y = np.array(data['pl_values'])[sorter]
            plt.plot(x, y, 'o-',label=f"Distance $d={d}$")

        
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel("Physical Error Rate ($p$)")
        plt.ylabel("Logical Error Rate ($P_L$)")
        plt.title(f"{title} Logical Error Rate vs. Physical Error Rate")
        plt.grid(True, which="both", ls="--")
        plt.legend()
        plt.show()


def run_bacon_shor_simulation(physerrorprobs):
    tasks = []
    for p in physerrorprobs:
        circuit = bacon_shor_circuit(5, p, add_Errors=True)
        
        # Add the task to Sinter's list
        tasks.append(sinter.Task(
                circuit=circuit,
                json_metadata={
                    'd': 5,
                    'p': p,
                }
            ))
    print(f"Generated {len(tasks)} tasks.")
    print("--- Starting sinter.collect (this may take a while) ---")
    start_time = time.time()
    collected_samples: list[sinter.AnonTaskStats()] = sinter.collect(
        num_workers=multiprocessing.cpu_count(),
        tasks=tasks,
        decoders=['pymatching'],
        max_errors=500,        # Collect 500 errors for good stats
        max_shots=100_000_000, # Safety cap (100 million)
        print_progress=True,
    )
    
    end_time = time.time()
    print(f"\n--- Sinter finished successfully in {end_time - start_time:.2f}s ---")

    return collected_samples




