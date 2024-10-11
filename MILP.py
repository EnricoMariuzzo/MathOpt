import gurobipy as gb

class MILP:
    def __init__(self, jobs, machines, times, demands, processing_times, weights, time_limit=None):
        self.jobs = jobs
        self.machines = machines
        self.times = times
        self.demands = demands
        self.processing_times = processing_times
        self.weights = weights
        self.schedule = {} 
        
        self.model = gb.Model("Job Scheduling")
        self.model.modelSense = gb.GRB.MINIMIZE
        self.model.setParam('outputFlag', 0)
        self.model.setParam("Threads", 4)

        if time_limit is not None:
            self.model.setParam('TimeLimit', time_limit)
        
        self.s = self.model.addVars(
            [(j,i,t) for j in self.jobs for i in self.machines for t in self.times], vtype=gb.GRB.BINARY
        )
        
        self.c = self.model.addVars(
            [j for j in self.jobs], lb=0.0
        )
        
        
        
    def set_objective(self):
        self.model.setObjective(
            gb.quicksum(self.weights[j] * self.c[j] for j in self.jobs)
        )
        
        
        
    def add_constraints(self):
        #vincolo di completamento
        for j in self.jobs:
            for i in self.machines:
                for t in self.times:
                    self.model.addConstr(t * self.s[j,i,t] + self.processing_times[j] <= self.c[j])
                    
        #vincolo di assegnazione unica
        for j in self.jobs:
            self.model.addConstr(gb.quicksum(self.s[j,i,t] for i in self.machines for t in self.times) == 1)
                    
        #vincolo di capacità
        for i in self.machines:
            for t in self.times:
                self.model.addConstr(gb.quicksum(
                    self.demands[j] * (gb.quicksum(self.s[j,i,v] for v in range(max(0, t - self.processing_times[j] + 1), t+1, 1)))
                    for j in self.jobs) <= 1)   
                
    
    
    def solve(self):
        self.model.optimize()
        
        if self.model.status == gb.GRB.OPTIMAL:
            for j in self.jobs:
                for i in self.machines:
                    for t in self.times:
                        if(self.s[j,i,t].x == 1):
                            self.schedule[j] = (i, t)
            return self.schedule
        else:
            return None