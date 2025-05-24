import os
import numpy as np
from src.simulation_runner import run_all
from src.plot_utils import generate_all_plots
from src.analysis_utils import generate_mm1_theoretical_table, compare_theory_vs_simulation

def ensure_directories():
    os.makedirs("data", exist_ok=True)
    os.makedirs("plots", exist_ok=True)

def main():
    print("Starting Queue Simulation Project")

    ensure_directories()

    run_all()

    generate_all_plots()

    lambda_values = np.arange(0.1, 0.95, 0.05)
    mu = 1.0
    theory_df = generate_mm1_theoretical_table(lambda_values, mu)

    compare_theory_vs_simulation(
        sim_file="data/mm1_results.csv",
        theory_df=theory_df,
        output_csv="data/theoretical_comparison.csv"
    )

    print("Simulation pipeline completed successfully.")
    print("Results saved in /data and /plots")

if __name__ == "__main__":
    main()
