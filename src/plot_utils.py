import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_metric(df, x_col, y_col, yerr_col=None, title="", ylabel="", filename=""):
    plt.figure(figsize=(8, 5))
    if yerr_col and yerr_col in df.columns:
        plt.errorbar(df[x_col], df[y_col], yerr=df[yerr_col], fmt='-o', capsize=5)
    else:
        plt.plot(df[x_col], df[y_col], '-o')
    plt.grid(True)
    plt.title(title)
    plt.xlabel("λ (arrival rate)")
    plt.ylabel(ylabel)
    plt.tight_layout()
    os.makedirs("plots", exist_ok=True)
    plt.savefig(os.path.join("plots", filename))
    plt.close()

def plot_all_models(metric, ylabel, filename_suffix):
    models = ["mm1", "gm1", "mg1"]
    colors = ['r', 'g', 'b']
    plt.figure(figsize=(8, 5))

    for model, color in zip(models, colors):
        df = pd.read_csv(f"data/{model}_results.csv")
        if metric in df.columns:
            plt.plot(df["lambda"], df[metric], label=model.upper(), color=color, marker='o')

    plt.grid(True)
    plt.xlabel("λ (arrival rate)")
    plt.ylabel(ylabel)
    plt.title(f"Comparison of {ylabel} across Models")
    plt.legend()
    plt.tight_layout()
    os.makedirs("plots", exist_ok=True)
    plt.savefig(os.path.join("plots", f"{filename_suffix}.png"))
    plt.close()

def generate_all_plots():
    for model in ["mm1", "gm1", "mg1"]:
        df = pd.read_csv(f"data/{model}_results.csv")

        plot_metric(df, "lambda", "avg_response_time", "std_response_time",
                    f"Mean Response Time - {model.upper()}", "Mean Response Time", f"{model}_response_time.png")
        
        plot_metric(df, "lambda", "avg_waiting_time", "std_waiting_time",
                    f"Mean Waiting Time - {model.upper()}", "Mean Waiting Time", f"{model}_waiting_time.png")
        
        plot_metric(df, "lambda", "utilization", None,
                    f"Utilization - {model.upper()}", "Server Utilization", f"{model}_utilization.png")

    plot_all_models("avg_response_time", "Mean Response Time", "combined_response_time")
    plot_all_models("avg_waiting_time", "Mean Waiting Time", "combined_waiting_time")
    plot_all_models("utilization", "Server Utilization", "combined_utilization")
