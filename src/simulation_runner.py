import numpy as np
import pandas as pd
import math
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

from simulate_mm1 import simulate_mm1
from simulate_gm1 import simulate_gm1
from simulate_mg1 import simulate_mg1

mu = 1.0
num_customers = 1000000
lambda_values = np.arange(0.1, 1.0, 0.1)
num_repeats = 5000

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
    for seed in range(num_repeats):
        rng = np.random.default_rng(seed)

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

# Parallel-safe task wrapper
def run_model_for_lambda(args):
    model, lam, mu_rate, num_customers, num_repeats = args
    if model == "mm1":
        result = run_and_average(simulate_mm1, model_name="mm1", lambda_rate=lam, mu_rate=mu_rate, num_customers=num_customers)
    elif model == "gm1":
        result = run_and_average(simulate_gm1, model_name="gm1", lambda_rate=lam, mu_rate=mu_rate, num_customers=num_customers, inter_arrival_func=uniform_interarrival)
    elif model == "mg1":
        result = run_and_average(simulate_mg1, model_name="mg1", lambda_rate=lam, mu_rate=mu_rate, num_customers=num_customers, service_time_func=weibull_service)
    return (model, result)

# Main runner
def run_all_parallel():
    models = {
        "mm1": [],
        "gm1": [],
        "mg1": []
    }

    args_list = [(model, lam, mu, num_customers, num_repeats) for lam in lambda_values for model in ["mm1", "gm1", "mg1"]]

    print("🚀 Starting parallel simulations...")
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_model_for_lambda, args) for args in args_list]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Running simulations"):
            model, result = future.result()
            models[model].append(result)

    # Save results
    pd.DataFrame(models["mm1"]).to_csv("data/mm1_results.csv", index=False)
    pd.DataFrame(models["gm1"]).to_csv("data/gm1_results.csv", index=False)
    pd.DataFrame(models["mg1"]).to_csv("data/mg1_results.csv", index=False)
    print("✅ All parallel simulations done.")

if __name__ == "__main__":
    run_all_parallel()
