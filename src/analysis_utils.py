import pandas as pd
import numpy as np

def theoretical_mm1_metrics(lambda_rate, mu_rate):
    """
    Compute theoretical metrics for an M/M/1 queue.

    Returns a dict with:
    - avg_waiting_time (Wq)
    - avg_response_time (W)
    - utilization (ρ)
    """
    rho = lambda_rate / mu_rate
    if rho >= 1:
        return {
            "lambda": lambda_rate,
            "mu": mu_rate,
            "utilization": np.nan,
            "avg_waiting_time": np.nan,
            "avg_response_time": np.nan
        }

    Wq = (rho**2) / (lambda_rate * (1 - rho))
    W = 1 / (mu_rate - lambda_rate)
    return {
        "lambda": lambda_rate,
        "mu": mu_rate,
        "utilization": rho,
        "avg_waiting_time": Wq,
        "avg_response_time": W
    }

def generate_mm1_theoretical_table(lambda_values, mu):
    """
    Compute and return a DataFrame with theoretical results for a list of λ.
    """
    results = [theoretical_mm1_metrics(lam, mu) for lam in lambda_values]
    return pd.DataFrame(results)

def compare_theory_vs_simulation(sim_file, theory_df, output_csv="data/theoretical_comparison.csv"):
    """
    Merge theoretical and simulated results for M/M/1 and save comparison to CSV.
    """
    sim_df = pd.read_csv(sim_file)
    merged = sim_df.merge(theory_df, on=["lambda", "mu"], suffixes=("_sim", "_theory"))
    merged["error_response_time"] = np.abs(merged["avg_response_time_sim"] - merged["avg_response_time_theory"])
    merged["error_waiting_time"] = np.abs(merged["avg_waiting_time_sim"] - merged["avg_waiting_time_theory"])
    merged.to_csv(output_csv, index=False)
    return merged
