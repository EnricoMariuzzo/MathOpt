from utils import isFeasible

class WSPT:
    def __init__(self, jobs, machines, times, demands, processing_times, weights): 
        self.jobs = jobs
        self.machines = machines
        self.times = times
        self.demands = demands
        self.processing_times = processing_times
        self.weights = weights
        self.schedule = {} 
    
    
    
    def sort_jobs(self):
        self.jobs.sort(key=lambda j: self.processing_times[j] / self.weights[j])



    def run_algorithm(self): 
        self.sort_jobs()
        
        for j in self.jobs:
            for t in self.times:
                for i in self.machines:
                    if isFeasible(j, i, t, self.demands, self.processing_times, self.schedule):
                        self.schedule[j] = (i, t)
                        break
                if j in self.schedule:
                    break

        return self.schedule
