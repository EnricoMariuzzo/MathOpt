from Alg1 import WSVF  
from WSPT import WSPT
import math

class Hybrid_WSVF:
    def __init__(self, jobs, machines, times, demands, processing_times, weights):
        self.jobs = jobs
        self.machines = machines
        self.times = times
        self.demands = demands
        self.processing_times = processing_times
        self.weights = weights
        self.times = times
        self.schedule = {}



    def split_jobs(self):
        I_l = [j for j in self.jobs if self.demands[j] <= 0.5]
        I_h = [j for j in self.jobs if self.demands[j] > 0.5]
        return I_l, I_h



    def run_algorithm(self):
        I_l, I_h = self.split_jobs()

        M1 = math.ceil(2 * (len(self.machines) - 2) / 3) + 1
        M2 = len(self.machines) - M1

        wsvf = WSVF(I_l, list(range(1, M1 + 1)), self.times, self.demands, self.processing_times, self.weights)
        schedule_I_l = wsvf.run_algorithm()

        wspt = WSPT(I_h, list(range(M1 + 1, len(self.machines) + 1)), self.times, self.demands, self.processing_times, self.weights)
        schedule_I_h = wspt.run_algorithm()

        self.schedule.update(schedule_I_l)
        self.schedule.update(schedule_I_h)

        return self.schedule
