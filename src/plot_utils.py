import os
import pandas as pd
import matplotlib.pyplot as plt

# --- Global Styling ---
plt.rcParams.update({
    'figure.figsize':       (10, 4),
    'axes.spines.top':      False,
    'axes.spines.right':    False,
    'axes.grid':            True,
    'grid.linestyle':       '--',
    'grid.color':           '#EEEEEE',
    'grid.linewidth':       0.8,
    'lines.linewidth':      2,
    'lines.marker':         'o',
    'lines.markersize':     6,
    'legend.frameon':       False,
    'legend.fontsize':      'medium',
    'xtick.direction':      'out',
    'ytick.direction':      'out',
    'xtick.major.size':     0,
    'ytick.major.size':     0,
    'axes.titlepad':        12,
    'axes.labelpad':        8
})

# Ensure output directory exists
def _ensure_plots_dir():
    os.makedirs("plots", exist_ok=True)


def plot_metric(df, x_col, y_col, yerr_col=None, title="", ylabel="", filename=""):
    fig, ax = plt.subplots()

    if yerr_col and yerr_col in df.columns:
        ax.errorbar(df[x_col], df[y_col], yerr=df[yerr_col], fmt='-o', capsize=5)
    else:
        ax.plot(df[x_col], df[y_col])

    ax.set_xlabel(r'$\lambda$ (arrival rate)', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, pad=10)
    ax.set_ylim(bottom=0)

    # Save
    _ensure_plots_dir()
    fig.tight_layout()
    fig.savefig(os.path.join("plots", filename), dpi=150, bbox_inches='tight')
    plt.close(fig)


def plot_all_models(metric, ylabel, filename_suffix):
    models = ["mm1", "gm1", "mg1"]
    labels = ["M/M/1", "G/M/1", "M/G/1"]

    fig, ax = plt.subplots()
    for model, label in zip(models, labels):
        df = pd.read_csv(f"data/{model}_results.csv")
        if metric in df.columns:
            ax.plot(df["lambda"], df[metric], label=label)

    ax.set_xlabel(r'$\lambda$ (arrival rate)', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(f"Comparison of {ylabel} across Models", pad=10)
    ax.set_ylim(bottom=0)

    # Legend below plot
    ax.legend(ncol=3, bbox_to_anchor=(0.5, -0.25), loc='upper center')

    # Save
    _ensure_plots_dir()
    fig.tight_layout()
    fig.savefig(os.path.join("plots", f"{filename_suffix}.png"), dpi=150, bbox_inches='tight')
    plt.close(fig)


def generate_all_plots():
    # Individual model plots
    for model in ["mm1", "gm1", "mg1"]:
        df = pd.read_csv(f"data/{model}_results.csv")

        plot_metric(
            df, "lambda", "avg_response_time", "std_response_time",
            f"Mean Response Time - {model.upper()}", "Mean Response Time", f"{model}_response_time.png"
        )
        plot_metric(
            df, "lambda", "avg_waiting_time", "std_waiting_time",
            f"Mean Waiting Time - {model.upper()}", "Mean Waiting Time", f"{model}_waiting_time.png"
        )
        plot_metric(
            df, "lambda", "utilization", None,
            f"Utilization - {model.upper()}", "Server Utilization", f"{model}_utilization.png"
        )

    # Combined comparison plots
    plot_all_models("avg_response_time", "Mean Response Time", "combined_response_time")
    plot_all_models("avg_waiting_time", "Mean Waiting Time", "combined_waiting_time")
    plot_all_models("utilization", "Server Utilization", "combined_utilization")
