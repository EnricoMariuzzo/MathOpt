def isFeasible(job, machine, start_time, demands, processing_times, schedule):
    """
    Verifica se il job può essere assegnato alla macchina rispettando i vincoli di capacità.
    
    Args:
    - job: L'ID del job corrente.
    - machine: L'ID della macchina.
    - start_time: L'istante di tempo in cui si vuole assegnare il job.
    - demands: Un dizionario {job_id: domanda del job}.
    - processing_times: Un dizionario {job_id: tempo di lavorazione del job}.
    - schedule: Un dizionario {job_id: (machine, start_time)} che rappresenta lo schedule corrente.

    Returns:
    - True se il job può essere assegnato, False altrimenti.
    """
    
    for t_prime in range(start_time, start_time + processing_times[job]):

        G_i_t_prime = [j for j, (m_j, s_j) in schedule.items() if m_j == machine and s_j <= t_prime < s_j + processing_times[j]]
        
        total_demand = sum(demands[h] for h in G_i_t_prime)
        
        if total_demand + demands[job] > 1:
            return False
    
    return True