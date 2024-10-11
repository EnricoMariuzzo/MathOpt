import random
import time
import numpy as np
import gurobipy as gb
from MILP import MILP
from Alg1 import WSVF
from Alg2 import Hybrid_WSVF


"""
Analisi di scalabilità degli algoritmi offline
"""

TIME_LIMIT = 300 #secondi


def generate_instance(N, M, seed):
    random.seed(seed)
    
    jobs = list(range(1, N + 1))
    machines = list(range(1, M + 1))
    weights = {j: random.randint(1, 10) for j in jobs}
    processing_times = {j: random.randint(1, 6) for j in jobs}
    demands = {j: round(random.uniform(0.1, 0.5), 2) for j in jobs}
    T = sum(processing_times.values())
    times = list(range(0, T + 1))
    
    return jobs, machines, times, weights, processing_times, demands



def measure_algorithm(algorithm, jobs, machines, times, demands, processing_times, weights):
    if algorithm == 'MILP':
        milp = MILP(jobs, machines, times, demands, processing_times, weights, TIME_LIMIT)
        milp.set_objective()
        milp.add_constraints()
        schedule = milp.solve()
        execution_time = milp.model.Runtime 
        weighted_completion_time = milp.model.objVal
        if schedule:
            mip_gap = 0.000
        else:
            if milp.model.status == gb.GRB.TIME_LIMIT:
                mip_gap = milp.model.MIPGap        
    else:
        start_time = time.time()
        if algorithm == 'WSVF':
            wsvf = WSVF(jobs, machines, times, demands, processing_times, weights)
            schedule = wsvf.run_algorithm()
        elif algorithm == 'HybridWSVF':
            hybrid_wsvf = Hybrid_WSVF(jobs, machines,times, demands, processing_times, weights)
            schedule = hybrid_wsvf.run_algorithm()
        else:
            raise ValueError(f"Algoritmo {algorithm} non riconosciuto")
        
        end_time = time.time()
        execution_time = end_time - start_time

        weighted_completion_time = 0
        if schedule:
            for job, (machine, start_time) in schedule.items():
                completion_time = start_time + processing_times[job]
                weighted_completion_time += weights[job] * completion_time
        
        mip_gap = None
    
    return execution_time, weighted_completion_time, mip_gap



def analyze_scalability(N, M, num_runs=10):
    milp_runtime_values = []
    wsvf_runtime_values = []
    hybrid_runtime_values = []

    gap_wsvf_values = []
    gap_hybrid_values = []
    
    wsvf_optimal_count = 0
    hybrid_optimal_count = 0
    
    milp_mip_gaps = []
    
    for run in range(num_runs):
        jobs, machines, times, weights, processing_times, demands = generate_instance(N, M, seed=run)

        milp_runtime, milp_completion_time, mip_gap = measure_algorithm('MILP', jobs, machines, times, demands, processing_times, weights)
        milp_runtime_values.append(milp_runtime)
        milp_mip_gaps.append(mip_gap)
        
        wsvf_runtime, wsvf_completion_time, _ = measure_algorithm('WSVF', jobs, machines, times, demands, processing_times, weights)
        wsvf_runtime_values.append(wsvf_runtime)
        gap_wsvf_values.append((wsvf_completion_time - milp_completion_time) / milp_completion_time)

        if (wsvf_completion_time == milp_completion_time):
            wsvf_optimal_count += 1 

        hybrid_runtime, hybrid_completion_time, _ = measure_algorithm('HybridWSVF', jobs, machines, times, demands, processing_times, weights)
        hybrid_runtime_values.append(hybrid_runtime)
        gap_hybrid_values.append((hybrid_completion_time - milp_completion_time) / milp_completion_time)

        if (hybrid_completion_time == milp_completion_time):
            hybrid_optimal_count += 1 

    milp_runtime_mean = np.mean(milp_runtime_values)
    milp_runtime_std = np.std(milp_runtime_values)

    wsvf_time_mean = np.mean(wsvf_runtime_values)
    wsvf_time_std = np.std(wsvf_runtime_values)
    wsvf_gap_mean = np.mean(gap_wsvf_values)
    wsvf_gap_std = np.std(gap_wsvf_values)

    hybrid_runtime_mean = np.mean(hybrid_runtime_values)
    hybrid_runtime_std = np.std(hybrid_runtime_values)
    hybrid_gap_mean = np.mean(gap_hybrid_values)
    hybrid_gap_std = np.std(gap_hybrid_values)
    
    mip_gap_mean = np.mean(milp_mip_gaps)
    mip_gap_std = np.std(milp_mip_gaps)
    
    return {
        'MILP': {'time_mean': milp_runtime_mean, 'time_std': milp_runtime_std, 'mip_mean': mip_gap_mean, 'mip_std': mip_gap_std},
        'WSVF': {'time_mean': wsvf_time_mean, 'time_std': wsvf_time_std, 'gap_mean': wsvf_gap_mean, 'gap_std': wsvf_gap_std, 
                 'optimal_count': wsvf_optimal_count},
        'HybridWSVF': {'time_mean': hybrid_runtime_mean, 'time_std': hybrid_runtime_std, 'gap_mean': hybrid_gap_mean, 
                       'gap_std': hybrid_gap_std, 'optimal_count': hybrid_optimal_count}
    }
    
    
#circa 7,5 ore 
for N in [10, 20, 30, 40 ,50]:
    for M in [2, 4, 6]:
        results = analyze_scalability(N, M)
        
        print(f"\nRisultati per N={N}, M={M}:")
        print(f"MILP - Tempo medio: {results['MILP']['time_mean']:.3f} sec, DevStd tempo: {results['MILP']['time_std']:.3f}, "
              f"MIP Gap medio: {results['MILP']['mip_mean']:.3f}, DevStd MIP: {results['MILP']['mip_std']:.3f}")
        print(f"WSVF - Tempo medio: {results['WSVF']['time_mean']:.3f} sec, DevStd tempo: {results['WSVF']['time_std']:.3f}, "
              f"Gap medio: {results['WSVF']['gap_mean']:.3f}, DevStd gap: {results['WSVF']['gap_std']:.3f}, "
              f"Soluzioni Ottime: {results['WSVF']['optimal_count']}/10")
        print(f"HybridWSVF - Tempo medio: {results['HybridWSVF']['time_mean']:.3f} sec, "
              f"Deviazione standard: {results['HybridWSVF']['time_std']:.3f}, Gap medio: {results['HybridWSVF']['gap_mean']:.3f}, "
              f"DevStd gap: {results['HybridWSVF']['gap_std']:.3f}, Soluzioni Ottime: {results['HybridWSVF']['optimal_count']}/10 \n")
        print("-" * 50)