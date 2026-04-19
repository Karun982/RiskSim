from simulation.monte_carlo import run_simulation
from simulation.risk_metrics import calculate_metrics

r = run_simulation(100000, 10, 'stocks')
metrics = calculate_metrics(r['final_values'], 100000)
print(metrics)
