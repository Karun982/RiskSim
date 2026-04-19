import numpy as np

# Historical mean return and volatility per asset class
ASSET_PARAMS = {
    "stocks":       {"mean": 0.10, "std": 0.18},
    "mutual_funds": {"mean": 0.08, "std": 0.12},
    "crypto":       {"mean": 0.25, "std": 0.70},
    "bonds":        {"mean": 0.04, "std": 0.05},
    "gold":         {"mean": 0.06, "std": 0.15},
}

def run_simulation(amount: float, years: int, asset_type: str, n_simulations: int = 1000):
    """
    Run Monte Carlo simulation for an investment.

    Args:
        amount: Initial investment amount
        years: Investment horizon in years
        asset_type: One of the keys in ASSET_PARAMS
        n_simulations: Number of simulation paths to generate

    Returns:
        dict with all paths and summary statistics
    """
    params = ASSET_PARAMS.get(asset_type, ASSET_PARAMS["stocks"])
    mu = params["mean"]
    sigma = params["std"]

    all_paths = []
    final_values = []

    for _ in range(n_simulations):
        portfolio = amount
        path = [round(portfolio, 2)]
        for _ in range(years):
            annual_return = np.random.normal(mu, sigma)
            portfolio *= (1 + annual_return)
            portfolio = max(portfolio, 0)  # Can't go below zero
            path.append(round(portfolio, 2))
        all_paths.append(path)
        final_values.append(portfolio)

    final_values = np.array(final_values)

    # Sample 100 paths for frontend (avoid sending all 1000)
    sample_indices = np.random.choice(len(all_paths), size=min(100, n_simulations), replace=False)
    sampled_paths = [all_paths[i] for i in sample_indices]

    # Key percentile paths
    sorted_indices = np.argsort(final_values)
    p10_path = all_paths[sorted_indices[int(0.10 * n_simulations)]]
    p50_path = all_paths[sorted_indices[int(0.50 * n_simulations)]]
    p90_path = all_paths[sorted_indices[int(0.90 * n_simulations)]]

    return {
        "final_values": final_values.tolist(),
        "sampled_paths": sampled_paths,
        "percentile_paths": {
            "p10": p10_path,
            "p50": p50_path,
            "p90": p90_path,
        },
        "labels": list(range(years + 1)),
        "meta": {
            "amount": amount,
            "years": years,
            "asset_type": asset_type,
            "n_simulations": n_simulations,
        }
    }