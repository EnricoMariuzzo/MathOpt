from utils import isFeasible

class BatchDispatchWSVF:
    """
    Tie-Breaking gestiti con strategia First Index Fit: 
    quando sono disponibili più macchine per lo scheduling di un job, viene scelta quella con indice più piccolo.
    """
    
    def __init__(self, jobs, machines, times, demands, processing_times, weights, release_times):
        self.jobs = jobs
        self.machines = machines
        self.times = times
        self.demands = demands
        self.processing_times = processing_times
        self.weights = weights
        self.release_times = release_times  # Tempo di arrivo dei job
        self.schedule = {}
    
    
    
    def sort_jobs(self, jobs):
        return sorted(jobs, key=lambda j: (self.processing_times[j] * self.demands[j]) / self.weights[j])



    def run_algorithm(self):
        for t_hat in self.times:
            available_jobs = [j for j in self.jobs if self.release_times[j] <= t_hat and j not in self.schedule]

            if not available_jobs:
                continue  # Se non ci sono job disponibili passa al prossimo intervallo

            sorted_jobs = self.sort_jobs(available_jobs)

            for j in sorted_jobs:
                for t_star in range(t_hat, max(self.times) + 1):
                    for i_star in self.machines:
                        if isFeasible(j, i_star, t_star, self.demands, self.processing_times, self.schedule):
                            self.schedule[j] = (i_star, t_star)
                            break
                    if j in self.schedule:
                        break

        return self.schedule