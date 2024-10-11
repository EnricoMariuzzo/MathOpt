from utils import isFeasible

class ContinuousWSVF_BestFit:
    """
    Tie-Breaking gestiti con strategia Best Fit: 
    quando sono disponibili più macchine per lo scheduling di un job, viene scelta quella con la capacità inutilizzata minore.
    """
    
    def __init__(self, jobs, machines, times, demands, processing_times, weights, release_times):
        self.jobs = jobs
        self.machines = machines
        self.times = times
        self.demands = demands
        self.processing_times = processing_times
        self.weights = weights
        self.release_times = release_times
        self.schedule = {}
    
    
    
    def sort_jobs(self, jobs):
        return sorted(jobs, key=lambda j: (self.processing_times[j] * self.demands[j]) / self.weights[j])



    def get_available_partition(self, machine, t_start, p_j):
        free_partition = 0
        
        for t in range(t_start, t_start + p_j):
            current_demand = 0
            
            for job, (m_j, s_j) in self.schedule.items():
                if m_j == machine and s_j <= t < s_j + self.processing_times[job]:
                    current_demand += self.demands[job]
                    
            free_partition += 1 - current_demand 
            
        return free_partition



    def run_algorithm(self):
        for t_hat in self.times:
            available_jobs = [j for j in self.jobs if self.release_times[j] <= t_hat and j not in self.schedule]

            if not available_jobs:
                continue

            sorted_jobs = self.sort_jobs(available_jobs)

            for j in sorted_jobs:
                best_machine = None
                min_available_partition = float('inf')
                
                for i_star in self.machines:
                    if isFeasible(j, i_star, t_hat, self.demands, self.processing_times, self.schedule):
                        available_partition = self.get_available_partition(i_star, t_hat, self.processing_times[j])
                        
                        if available_partition < min_available_partition:
                            best_machine = i_star
                            min_available_partition = available_partition
                
                if best_machine is not None:
                    self.schedule[j] = (best_machine, t_hat)
                    
        return self.schedule