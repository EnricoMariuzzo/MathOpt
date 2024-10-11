import random
import time
import numpy as np
from Alg3 import BatchDispatchWSVF as Alg3
from Alg3_BestFit import BatchWSVF_BestFit as Alg3_BestFit
from Alg4 import ContinuousDispatchWSVF as Alg4
from Alg4_BestFit import ContinuousWSVF_BestFit as Alg4_BestFit

"""
Analisi delle performance degli algoritmi online con diverse strategie di Tie-Breaking
"""


def generate_instance(N, M, seed):
    random.seed(seed)
    jobs = list(range(1, N + 1))
    machines = list(range(1, M + 1))
    weights = {j: random.randint(1, 10) for j in range(1, N + 1)}
    processing_times = {j: random.randint(1, 6) for j in range(1, N + 1)}
    demands = {j: round(random.uniform(0.1, 0.5), 2) for j in range(1, N + 1)}
    release_times = {j: random.randint(1, 30) for j in jobs}
    T = sum(processing_times.values())
    times = list(range(0, T + 1))
    return jobs, machines, times, demands, processing_times, weights, release_times  



def execute_algorithm(algorithm_class, jobs, machines, times, demands, processing_times, weights, release_times):
    start_time = time.time()
    algorithm = algorithm_class(jobs, machines, times, demands, processing_times, weights, release_times)
    schedule = algorithm.run_algorithm()
    end_time = time.time()
    
    execution_time = end_time - start_time
    weighted_completion_time = 0
    for job, (machine, start_time) in schedule.items():
        completion_time = start_time + processing_times[job]
        weighted_completion_time += weights[job] * completion_time
    
    return execution_time, weighted_completion_time



def compare_algorithms(N_values, M_values, num_runs):
    results = []

    for N in N_values:
        for M in M_values:
            alg3_times, alg3_wcts = [], []
            alg3_bf_times, alg3_bf_wcts = [], []
            alg4_times, alg4_wcts = [], []
            alg4_bf_times, alg4_bf_wcts = [], []
            
            for run in range(1, num_runs + 1):
                jobs, machines, times, demands, processing_times, weights, release_times = generate_instance(N, M, run)

                exec_time_alg3, wct_alg3 = execute_algorithm(Alg3, jobs, machines, times, demands, processing_times, weights, release_times)
                alg3_times.append(exec_time_alg3)
                alg3_wcts.append(wct_alg3)
                
                exec_time_alg3_bf, wct_alg3_bf = execute_algorithm(Alg3_BestFit, jobs, machines, times, demands, processing_times, weights, release_times)
                alg3_bf_times.append(exec_time_alg3_bf)
                alg3_bf_wcts.append(wct_alg3_bf)
                
                exec_time_alg4, wct_alg4 = execute_algorithm(Alg4, jobs, machines, times, demands, processing_times, weights, release_times)
                alg4_times.append(exec_time_alg4)
                alg4_wcts.append(wct_alg4)
                
                exec_time_alg4_bf, wct_alg4_bf = execute_algorithm(Alg4_BestFit, jobs, machines, times, demands, processing_times, weights, release_times)
                alg4_bf_times.append(exec_time_alg4_bf)
                alg4_bf_wcts.append(wct_alg4_bf)
                
            results.append({
                "N": N, "M": M,
                "Alg3_Avg_Time": np.mean(alg3_times), "Alg3_Std_Time": np.std(alg3_times),
                "Alg3_Avg_WCT": np.mean(alg3_wcts), "Alg3_Std_WCT": np.std(alg3_wcts),
                "Alg3_BF_Avg_Time": np.mean(alg3_bf_times), "Alg3_BF_Std_Time": np.std(alg3_bf_times),
                "Alg3_BF_Avg_WCT": np.mean(alg3_bf_wcts), "Alg3_BF_Std_WCT": np.std(alg3_bf_wcts),
                "Alg4_Avg_Time": np.mean(alg4_times), "Alg4_Std_Time": np.std(alg4_times),
                "Alg4_Avg_WCT": np.mean(alg4_wcts), "Alg4_Std_WCT": np.std(alg4_wcts),
                "Alg4_BF_Avg_Time": np.mean(alg4_bf_times), "Alg4_BF_Std_Time": np.std(alg4_bf_times),
                "Alg4_BF_Avg_WCT": np.mean(alg4_bf_wcts), "Alg4_BF_Std_WCT": np.std(alg4_bf_wcts)
            })

    return results


#circa 6 ore
N_values = [1000, 1500, 2000] 
M_values = [10, 20, 30]       
num_runs = 10            

results = compare_algorithms(N_values, M_values, num_runs)

for result in results:
    print(f"N={result['N']}, M={result['M']}")
    print(f"Alg3 - Tempo medio: {result['Alg3_Avg_Time']:.3f} sec, DevStd tempo: {result['Alg3_Std_Time']:.3f}, WCT medio: {result['Alg3_Avg_WCT']:.0f}, DevStd WCT: {result['Alg3_Std_WCT']:.0f}")
    print(f"Alg3 Best Fit - Tempo medio: {result['Alg3_BF_Avg_Time']:.3f} sec, DevStd tempo: {result['Alg3_BF_Std_Time']:.3f}, WCT medio: {result['Alg3_BF_Avg_WCT']:.0f}, DevStd WCT: {result['Alg3_BF_Std_WCT']:.0f}")
    print(f"Alg4 - Tempo medio: {result['Alg4_Avg_Time']:.3f} sec, DevStd tempo: {result['Alg4_Std_Time']:.3f}, WCT medio: {result['Alg4_Avg_WCT']:.0f}, DevStd WCT: {result['Alg4_Std_WCT']:.0f}")
    print(f"Alg4 Best Fit - Tempo medio: {result['Alg4_BF_Avg_Time']:.3f} sec, DevStd tempo: {result['Alg4_BF_Std_Time']:.3f}, WCT medio: {result['Alg4_BF_Avg_WCT']:.0f}, DevStd WCT: {result['Alg4_BF_Std_WCT']:.0f}")
    print("-" * 50)
