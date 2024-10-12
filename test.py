import random
import time
import gurobipy as gb
from MILP import MILP
from Alg1 import WSVF
from WSPT import WSPT
from Alg2 import Hybrid_WSVF
from Alg3 import BatchDispatchWSVF
from Alg3_BestFit import BatchWSVF_BestFit
from Alg4 import ContinuousDispatchWSVF
from Alg4_BestFit import ContinuousWSVF_BestFit



def generate_instance(N, M, seed):
    random.seed(seed)
    jobs = list(range(1, N + 1))
    machines = list(range(1, M + 1))
    weights = {j: random.randint(1, 10) for j in jobs}
    processing_times = {j: random.randint(1, 6) for j in jobs}
    demands = {j: round(random.uniform(0.1, 0.5), 2) for j in jobs}
    release_times = {j: random.randint(1, 30) for j in jobs}
    T = sum(processing_times.values())
    times = list(range(0, T + 1))
    
    return jobs, machines, times, demands, processing_times, weights, release_times



def run_milp(jobs, machines, times, demands, processing_times, weights, time_limit=None):
    milp = MILP(jobs, machines, times, demands, processing_times, weights, time_limit)
    milp.set_objective()
    milp.add_constraints()
    schedule = milp.solve()
   
    if schedule:
        for job, (machine, start_time) in schedule.items():
            print(f"Job {job} assegnato alla macchina {machine} all'istante {start_time}.")
            
        print(f"\nValore ottimo della funzione obiettivo: {milp.model.objVal}")
        print(f"Tempo totale di esecuzione: {round(milp.model.Runtime, 3)} secondi")
    else:
        if milp.model.status == gb.GRB.TIME_LIMIT:
            print(f"\nWeighted Completion time: {milp.model.objVal}")
            print(f"Tempo totale di esecuzione: {round(milp.model.Runtime, 3)} secondi")
            print(f"MIP GAP: {milp.model.MIPGap:.3f}\n")
        else:
            print("Non è stata trovata una soluzione ottima.")



def run_heuristic(algorithm_class, jobs, machines, times, demands, processing_times, weights, release_times=None):
    start_time = time.time()
    if release_times is not None:
        heuristic = algorithm_class(jobs, machines, times, demands, processing_times, weights, release_times)
    else:
        heuristic = algorithm_class(jobs, machines, times, demands, processing_times, weights)
    schedule = heuristic.run_algorithm()
    end_time = time.time()
    
    execution_time = end_time - start_time
    weighted_completion_time = sum(weights[j] * (schedule[j][1] + processing_times[j]) for j in schedule.keys())
    
    for job, (machine, start_time) in schedule.items():
        print(f"Job {job} assegnato alla macchina {machine} all'istante {start_time}.")

    print(f"\nWeighted Completion Time: {weighted_completion_time}")
    print(f"Tempo di esecuzione dell'algoritmo: {execution_time:.3f} secondi")



def run_tests():
    N = 10  # Numero di job
    M = 2   # Numero di macchine
    seed = 15
    time_limit = 300 

    jobs, machines, times, demands, processing_times, weights, release_times = generate_instance(N, M, seed)

    print("Esecuzione del MILP...")
    run_milp(jobs, machines, times, demands, processing_times, weights, time_limit)
    print("-" * 50)

    print("Esecuzione del WSVF...")
    run_heuristic(WSVF, jobs, machines, times, demands, processing_times, weights)
    print("-" * 50)
    
    print("Esecuzione del WSPT...")
    run_heuristic(WSPT, jobs, machines, times, demands, processing_times, weights)
    print("-" * 50)

    print("Esecuzione dell'Hybrid-WSVF...")
    run_heuristic(Hybrid_WSVF, jobs, machines, times, demands, processing_times, weights)
    print("-" * 50)

    print("Esecuzione del Batch Dispatch WSVF...")
    run_heuristic(BatchDispatchWSVF, jobs, machines, times, demands, processing_times, weights, release_times)
    print("-" * 50)

    print("Esecuzione del Batch Dispatch WSVF Best Fit...")
    run_heuristic(BatchWSVF_BestFit, jobs, machines, times, demands, processing_times, weights, release_times)
    print("-" * 50)

    print("Esecuzione del Continuous Dispatch WSVF...")
    run_heuristic(ContinuousDispatchWSVF, jobs, machines, times, demands, processing_times, weights, release_times)
    print("-" * 50)

    print("Esecuzione del Continuous Dispatch WSVF Best Fit...")
    run_heuristic(ContinuousWSVF_BestFit, jobs, machines, times, demands, processing_times, weights, release_times)
    print("-" * 50)



if __name__ == "__main__":
    run_tests()
