Implementazione del paper: 
"Cohen, I. R., Cohen, I., & Zaks, I. (2023). A theoretical and empirical study of job scheduling in cloud computing environments: 
the weighted completion time minimization problem with capacitated parallel machines. Annals of Operations Research"

- MILP.py contiene l'implementazione del modello esatto
- utils.py contiene l'implementazione della funzione "IsFeasible" (usata in Alg1, Alg3, Alg4)
- Alg1-Alg2.py contengono l'implementazione degli algoritmi per ambiente offline
- WSPT.py contiene l'implementazione dell'algoritmo WSPT (non descritto nel paper ma utilizzato in Alg2)
- Alg3-Alg4.py contengono l'implementazione degli algoritmi per ambiente online (con strategia di tie-breaking First Index Fit)
- Alg3_BestFit-Alg4_BestFit.py contengono l'implementazione degli algoritmi per ambiente online (con strategia di tie-breaking Best Fit)
- test.py contiene l'esecuzione su una piccola istanza del modello esatto e di tutti gli algoritmi 
- scalability.py contiene l'analisi di scalabilità degli algoritmi offline e del modello esatto
- online_performance.py contiene l'analisi delle performance degli algoritmi online 
