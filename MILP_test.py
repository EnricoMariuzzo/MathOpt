import random
from MILP import MILP
import gurobipy as gb

random.seed(15)

N = 10  # numero di job
M = 2  # numero di macchine
time_limit = 60 #secondi

jobs = list(range(1, N + 1))
machines = list(range(1, M + 1))
weights = {j: random.randint(1, 10) for j in range(1, N + 1)}
processing_times = {j: random.randint(1, 6) for j in range(1, N + 1)}
demands = {j: round(random.uniform(0.1, 0.5), 2) for j in range(1, N + 1)}

T = sum(processing_times.values())
times = list(range(0, T + 1))

milp = MILP(jobs, machines, times, demands, processing_times, weights, time_limit)
milp.set_objective()
milp.add_constraints()
schedule = milp.solve()
         
if schedule:
    print(f"\nValore ottimo della funzione obiettivo: {milp.model.objVal}")
    print(f"Tempo totale di esecuzione: {round(milp.model.Runtime, 3)} secondi\n")
    
    for job, (machine, start_time) in schedule.items():
        print(f"Job {job} assegnato alla macchina {machine} all'istante {start_time}.")
else:
    if milp.model.status == gb.GRB.TIME_LIMIT:
        print(f"\nWeighted Completion time: {milp.model.objVal}")
        print(f"Tempo totale di esecuzione: {round(milp.model.Runtime, 3)} secondi")
        print(f"MIP GAP: {milp.model.MIPGap:.3f}\n")
    else:
        print("Non è stata trovata una soluzione ottima.")