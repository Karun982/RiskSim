import numpy as np


def calculate_metrics(final_values: list, initial_amount: float) -> dict:
    """
    Calculate risk metrics from simulation final values.

    Args:
        final_values: List of final portfolio values from simulation
        initial_amount: The original investment amount

    Returns:
        dict with all risk metrics
    """
    arr = np.array(final_values)

    avg         = float(np.mean(arr))
    median      = float(np.median(arr))
    best        = float(np.percentile(arr, 95))   # Top 5%
    worst       = float(np.percentile(arr, 5))    # Bottom 5%
    loss_prob   = float(np.mean(arr < initial_amount) * 100)
    total_gain  = ((avg - initial_amount) / initial_amount) * 100

    # Distribution buckets for histogram
    distribution = sorted([round(v, 2) for v in arr.tolist()])

    return {
        "avg":          round(avg, 2),
        "median":       round(median, 2),
        "best":         round(best, 2),
        "worst":        round(worst, 2),
        "loss_prob":    round(loss_prob, 1),
        "total_gain":   round(total_gain, 1),
        "initial":      initial_amount,
        "distribution": distribution,
    }