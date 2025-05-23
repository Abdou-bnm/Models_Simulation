import numpy as np
import pandas as pd
from tqdm import tqdm
import math

from src.simulate_mm1 import simulate_mm1
from src.simulate_gm1 import simulate_gm1
from src.simulate_mg1 import simulate_mg1

# Configuration
mu = 1.0
num_customers = 10000
lambda_values = np.arange(0.1, 1.0, 0.1)
num_repeats = 100

# Inter-arrival time for G/M/1 (uniform)
def uniform_interarrival(lambda_rate, rng):
    return rng.uniform(0.5 / lambda_rate, 1.5 / lambda_rate)

# Service time for M/G/1 (Weibull with scale normalized to mean=1/μ)
def weibull_service(mu_rate, rng):
    k = 1.5
    scale = (1 / mu_rate) / math.gamma(1 + 1 / k)
    return rng.weibull(k) * scale

# Run multiple seeds for one model and average results
def run_and_average(sim_func, model_name="", lambda_rate=0.1, **kwargs):
    results = []
    desc = f"{model_name.upper()} λ={lambda_rate:.2f}"
    for seed in tqdm(range(num_repeats), desc=desc, leave=False):
        rng = np.random.default_rng(seed)

        # Inject rng-compatible lambdas
        if "inter_arrival_func" in kwargs:
            kwargs["inter_arrival_func"] = lambda lam, r=rng: uniform_interarrival(lam, r)
        if "service_time_func" in kwargs:
            kwargs["service_time_func"] = lambda mu, r=rng: weibull_service(mu, r)

        metrics = sim_func(seed=seed, lambda_rate=lambda_rate, **kwargs)
        results.append(metrics)

    return {
        "lambda": lambda_rate,
        "mu": kwargs["mu_rate"],
        "avg_waiting_time": np.mean([r["avg_waiting_time"] for r in results]),
        "avg_response_time": np.mean([r["avg_response_time"] for r in results]),
        "utilization": np.mean([r["utilization"] for r in results]),
        "std_waiting_time": np.std([r["avg_waiting_time"] for r in results]),
        "std_response_time": np.std([r["avg_response_time"] for r in results])
    }

# Main runner
def run_all():
    models = {
        "mm1": [],
        "gm1": [],
        "mg1": []
    }

    print("🚀 Starting simulations...")
    for lam in tqdm(lambda_values, desc="λ sweep"):
        # M/M/1
        mm1_result = run_and_average(
            simulate_mm1,
            model_name="mm1",
            lambda_rate=lam,
            mu_rate=mu,
            num_customers=num_customers
        )
        models["mm1"].append(mm1_result)

        # G/M/1
        gm1_result = run_and_average(
            simulate_gm1,
            model_name="gm1",
            lambda_rate=lam,
            mu_rate=mu,
            num_customers=num_customers,
            inter_arrival_func=uniform_interarrival  # Will be wrapped properly
        )
        models["gm1"].append(gm1_result)

        # M/G/1
        mg1_result = run_and_average(
            simulate_mg1,
            model_name="mg1",
            lambda_rate=lam,
            mu_rate=mu,
            num_customers=num_customers,
            service_time_func=weibull_service  # Will be wrapped properly
        )
        models["mg1"].append(mg1_result)

    # Save results to CSV
    pd.DataFrame(models["mm1"]).to_csv("data/mm1_results.csv", index=False)
    pd.DataFrame(models["gm1"]).to_csv("data/gm1_results.csv", index=False)
    pd.DataFrame(models["mg1"]).to_csv("data/mg1_results.csv", index=False)
    print("✅ Simulations complete. Results saved in /data/")

if __name__ == "__main__":
    run_all()
