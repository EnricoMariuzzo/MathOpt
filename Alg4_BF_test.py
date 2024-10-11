import random
import time
from Alg4_BestFit import ContinuousWSVF_BestFit

random.seed(15)

N = 10  # numero di job
M = 2   # numero di macchine

jobs = list(range(1, N + 1))
machines = list(range(1, M + 1))
weights = {j: random.randint(1, 10) for j in jobs}
processing_times = {j: random.randint(1, 6) for j in jobs}
demands = {j: round(random.uniform(0.1, 0.5), 2) for j in jobs}
release_times = {j: random.randint(1, 30) for j in jobs}  

T = sum(processing_times.values())
times = list(range(0, T + 1))


start_time = time.time()

continuous_dispatch = ContinuousWSVF_BestFit(jobs, machines, times, demands, processing_times, weights, release_times)
schedule = continuous_dispatch.run_algorithm()

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