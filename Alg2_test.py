import random
from Alg2 import Hybrid_WSVF
import time

random.seed(15)

N = 10  # numero di job
M = 2 # numero di macchine

jobs = list(range(1, N + 1))
machines = list(range(1, M + 1))
weights = {j: random.randint(1, 10) for j in range(1, N + 1)}
processing_times = {j: random.randint(1, 6) for j in range(1, N + 1)}
demands = {j: round(random.uniform(0.1, 1), 2) for j in range(1, N + 1)}

T = sum(processing_times.values())
times = list(range(0, T + 1))

start_time = time.time()

hybrid_wsvf = Hybrid_WSVF(jobs, machines, times, demands, processing_times, weights)
schedule = hybrid_wsvf.run_algorithm()

end_time = time.time()
execution_time = end_time - start_time


weighted_completion_time = 0
for job, (machine, start_time) in schedule.items():
    completion_time = start_time + processing_times[job]
    weighted_completion_time += weights[job] * completion_time

print("\nSchedule ottenuto:")
for job, (machine, start_time) in schedule.items():
    print(f"Job {job} assegnato alla macchina {machine} all'istante {start_time}.")

print(f"\nWeighted Completion Time: {weighted_completion_time}")
print(f"Tempo di esecuzione dell'algoritmo: {execution_time:.3f} secondi")