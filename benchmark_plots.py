import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Configuration ─────────────────────────────────────────────────────────────

INPUT_DIR  = "."
OUTPUT_DIR = "."

COLORS = {
    "next_fit":             "#E63946",
    "first_fit":            "#2196F3",
    "first_fit_decreasing": "#FF9800",
    "best_fit":             "#4CAF50",
    "best_fit_decreasing":  "#9C27B0",
}

ALGO_LABELS = {
    "next_fit":             "Next Fit",
    "first_fit":            "First Fit",
    "first_fit_decreasing": "First Fit Decreasing",
    "best_fit":             "Best Fit",
    "best_fit_decreasing":  "Best Fit Decreasing",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_avg_csv(algo_name: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (sizes, avg_time_ns, avg_waste) arrays."""
    path = os.path.join(INPUT_DIR, f"{algo_name}_avg.csv")
    sizes, times, wastes = [], [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sizes.append(int(row["size"]))
            times.append(float(row["avg_time_ns"]))
            wastes.append(float(row["avg_waste"]))
    return np.array(sizes), np.array(times), np.array(wastes)


def fit_line(sizes: np.ndarray, values: np.ndarray) -> tuple[float, float]:
    """Fit log2(values) ~ slope * log2(sizes) + intercept."""
    log_x = np.log2(sizes)
    log_y = np.log2(values)
    slope, intercept = np.polyfit(log_x, log_y, 1)
    return slope, intercept


def best_fit_line(sizes: np.ndarray, slope: float, intercept: float) -> np.ndarray:
    return 2 ** (slope * np.log2(sizes) + intercept)


def equation_label(algo_name: str, slope: float, intercept: float) -> str:
    coeff = 2 ** intercept
    label = ALGO_LABELS[algo_name]
    return f"{label}  |  T = {coeff:.3g}·n^{slope:.3f}  (slope={slope:.3f})"


def waste_label(algo_name: str, slope: float, intercept: float) -> str:
    coeff = 2 ** intercept
    label = ALGO_LABELS[algo_name]
    return f"{label}  |  W = {coeff:.3g}·n^{slope:.3f}  (slope={slope:.3f})"


def style_log_x(ax, sizes: np.ndarray):
    """Set x-axis to log2 scale with power-of-2 tick labels."""
    ax.set_xscale("log", base=2)
    powers = np.log2(sizes).astype(int)
    ticks = [2**p for p in range(powers.min(), powers.max() + 1)]
    ax.set_xticks(ticks)
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"$2^{{{int(np.log2(x))}}}$")
    )
    ax.set_xlabel("Input Size (n)", fontsize=11)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)
    ax.tick_params(axis="both", labelsize=9)


def save_plot(fig, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Saved {path}")


# ── Single-metric plots (time or waste) ───────────────────────────────────────

def plot_metric(algos: list[str], metric: str, title: str, filename: str):
    """
    metric: "time" or "waste"
    Plots scattered data points + dotted line of best fit for each algorithm.
    """
    ylabel = "Average Time (ns)" if metric == "time" else "Average Waste W(A)"
    all_sizes = None

    fig, ax = plt.subplots(figsize=(9, 6))

    for algo_name in algos:
        sizes, times, wastes = load_avg_csv(algo_name)
        if all_sizes is None:
            all_sizes = sizes

        values = times if metric == "time" else wastes
        slope, intercept = fit_line(sizes, values)
        fitted = best_fit_line(sizes, slope, intercept)
        color = COLORS[algo_name]

        label_fn = equation_label if metric == "time" else waste_label
        ax.scatter(sizes, values, color=color, zorder=3, s=30)
        ax.plot(sizes, fitted, color=color, linestyle="--", linewidth=2,
                label=label_fn(algo_name, slope, intercept))

    ax.set_yscale("log", base=2)
    style_log_x(ax, all_sizes)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.legend(fontsize=8, loc="upper left")
    save_plot(fig, filename)


# ── Combined twin-axis plot (time + waste) ────────────────────────────────────

def plot_combined(algos: list[str], title: str, filename: str):
    """
    Left y-axis:  Average Time (ns)   — solid markers, dotted fit line
    Right y-axis: Average Waste W(A)  — hollow triangle markers, dash-dot fit line
    """
    all_sizes = None
    fig, ax_time = plt.subplots(figsize=(10, 6))
    ax_waste = ax_time.twinx()

    time_handles, waste_handles = [], []

    for algo_name in algos:
        sizes, times, wastes = load_avg_csv(algo_name)
        if all_sizes is None:
            all_sizes = sizes
        color = COLORS[algo_name]

        # ── Time (left axis) ──
        t_slope, t_intercept = fit_line(sizes, times)
        t_fitted = best_fit_line(sizes, t_slope, t_intercept)
        ax_time.scatter(sizes, times, color=color, zorder=3, s=30)
        h_time, = ax_time.plot(
            sizes, t_fitted, color=color, linestyle="--", linewidth=2,
            label=equation_label(algo_name, t_slope, t_intercept)
        )
        time_handles.append(h_time)

        # ── Waste (right axis) ──
        w_slope, w_intercept = fit_line(sizes, wastes)
        w_fitted = best_fit_line(sizes, w_slope, w_intercept)
        ax_waste.scatter(sizes, wastes, color=color, zorder=3, s=30,
                         marker="^", facecolors="none", edgecolors=color)
        h_waste, = ax_waste.plot(
            sizes, w_fitted, color=color, linestyle="-.", linewidth=1.5,
            label=waste_label(algo_name, w_slope, w_intercept)
        )
        waste_handles.append(h_waste)

    # Axes styling
    ax_time.set_yscale("log", base=2)
    ax_waste.set_yscale("log", base=2)
    style_log_x(ax_time, all_sizes)

    ax_time.set_ylabel("Average Time (ns)", fontsize=11)
    ax_waste.set_ylabel("Average Waste W(A)", fontsize=11)
    ax_waste.tick_params(axis="y", labelsize=9)

    ax_time.set_title(title, fontsize=13, fontweight="bold")

    # Two-section legend: time on top-left, waste on bottom-right
    legend_time = ax_time.legend(handles=time_handles, title="── Run Time",
                                  fontsize=7, loc="upper left")
    ax_time.legend(handles=waste_handles, title="·· Waste",
                   fontsize=7, loc="lower right")
    ax_time.add_artist(legend_time)

    save_plot(fig, filename)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── Next Fit ──────────────────────────────────────────────────────────────
    plot_metric(["next_fit"], "time",
                "Next Fit — Run Time", "next_fit_time.png")

    plot_metric(["next_fit"], "waste",
                "Next Fit — Waste W(A)", "next_fit_waste.png")

    plot_combined(["next_fit"],
                  "Next Fit — Run Time & Waste", "next_fit_combined.png")

    # ── Best Fit & Best Fit Decreasing ────────────────────────────────────────
    plot_metric(["best_fit", "best_fit_decreasing"], "time",
                "Best Fit & Best Fit Decreasing — Run Time",
                "best_fit_time.png")

    plot_metric(["best_fit", "best_fit_decreasing"], "waste",
                "Best Fit & Best Fit Decreasing — Waste W(A)",
                "best_fit_waste.png")

    plot_combined(["best_fit", "best_fit_decreasing"],
                  "Best Fit & Best Fit Decreasing — Run Time & Waste",
                  "best_fit_combined.png")

    # ── First Fit & First Fit Decreasing ──────────────────────────────────────
    plot_metric(["first_fit", "first_fit_decreasing"], "time",
                "First Fit & First Fit Decreasing — Run Time",
                "first_fit_time.png")

    plot_metric(["first_fit", "first_fit_decreasing"], "waste",
                "First Fit & First Fit Decreasing — Waste W(A)",
                "first_fit_waste.png")

    plot_combined(["first_fit", "first_fit_decreasing"],
                  "First Fit & First Fit Decreasing — Run Time & Waste",
                  "first_fit_combined.png")

    # ── All Algorithms ────────────────────────────────────────────────────────
    all_algos = ["next_fit", "first_fit", "first_fit_decreasing",
                 "best_fit", "best_fit_decreasing"]

    plot_metric(all_algos, "time",
                "All Algorithms — Run Time", "all_time.png")

    plot_metric(all_algos, "waste",
                "All Algorithms — Waste W(A)", "all_waste.png")

    plot_combined(all_algos,
                  "All Algorithms — Run Time & Waste", "all_combined.png")

    print("\nAll plots complete.")


if __name__ == "__main__":
    main()