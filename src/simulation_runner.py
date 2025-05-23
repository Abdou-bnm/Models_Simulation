import numpy as np
import pandas as pd
from tqdm import tqdm

from src.simulate_mm1 import simulate_mm1
from src.simulate_gm1 import simulate_gm1
from src.simulate_mg1 import simulate_mg1

# Configuration
mu = 1.0
num_customers = 100000
lambda_values = np.arange(0.1, 0.95, 0.05)
num_repeats = 10

# General distribution functions
def uniform_interarrival():
    return np.random.uniform(0.5, 1.5)  # mean ≈ 1

def weibull_service():
    return np.random.weibull(2)  # shape=2 (mean depends on scale)

def run_and_average(sim_func, **kwargs):
    results = []
    for seed in range(num_repeats):
        metrics = sim_func(seed=seed, **kwargs)
        results.append(metrics)
    return {
        "lambda": kwargs["lambda_rate"],
        "mu": kwargs["mu_rate"],
        "avg_waiting_time": np.mean([r["avg_waiting_time"] for r in results]),
        "avg_response_time": np.mean([r["avg_response_time"] for r in results]),
        "utilization": np.mean([r["utilization"] for r in results]),
        "std_waiting_time": np.std([r["avg_waiting_time"] for r in results]),
        "std_response_time": np.std([r["avg_response_time"] for r in results])
    }

def run_all():
    models = {
        "mm1": [],
        "gm1": [],
        "mg1": []
    }

    print("Running simulations...")
    for lam in tqdm(lambda_values, desc="λ sweep"):
        # M/M/1
        mm1_result = run_and_average(
            simulate_mm1,
            lambda_rate=lam,
            mu_rate=mu,
            num_customers=num_customers
        )
        models["mm1"].append(mm1_result)

        # G/M/1
        gm1_result = run_and_average(
            simulate_gm1,
            lambda_rate=lam,
            mu_rate=mu,
            num_customers=num_customers,
            inter_arrival_func=uniform_interarrival
        )
        models["gm1"].append(gm1_result)

        # M/G/1
        mg1_result = run_and_average(
            simulate_mg1,
            lambda_rate=lam,
            mu_rate=mu,
            num_customers=num_customers,
            service_time_func=weibull_service
        )
        models["mg1"].append(mg1_result)

    # Save to CSV
    pd.DataFrame(models["mm1"]).to_csv("data/mm1_results.csv", index=False)
    pd.DataFrame(models["gm1"]).to_csv("data/gm1_results.csv", index=False)
    pd.DataFrame(models["mg1"]).to_csv("data/mg1_results.csv", index=False)
    print("Simulations complete. Results saved in /data/")

if __name__ == "__main__":
    run_all()
