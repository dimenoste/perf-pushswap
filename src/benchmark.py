#!/usr/bin/env python3

import subprocess
import random
import time
import argparse
import os
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import shutil
import sys

# --------------------------
# Configuration
# --------------------------
MAX_INT = 1000  # default maximum integer in sequences

# --------------------------
# Utilities
# --------------------------

def count_inversions(nums):
    """Count all pair inversions (full-pair disorder)."""
    inv = 0
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] > nums[j]:
                inv += 1
    return inv


def compute_disorder(nums):
    """Compute disorder fraction 0.0–1.0 (matches C compute_disorder)."""
    n = len(nums)
    if n < 2:
        return 0.0
    total_pairs = n * (n - 1) // 2
    return count_inversions(nums) / total_pairs


def generate_list_with_target_disorder_fast(nums, target_fraction):
    """
    Generate a list with approximate full-pair disorder.
    target_fraction: 0.0 -> fully sorted, 1.0 -> fully reversed
    """
    n = len(nums)
    if n <= 1:
        return nums

    mid = n // 2
    left = generate_list_with_target_disorder_fast(nums[:mid], target_fraction)
    right = generate_list_with_target_disorder_fast(nums[mid:], target_fraction)

    merged = []
    while left and right:
        prob_right = target_fraction  # linear mapping
        if random.random() < prob_right:
            merged.append(right.pop(0))
        else:
            merged.append(left.pop(0))
    merged += left + right
    return merged


def generate_benchmark_list(size, target_fraction):
    """
    Generate a shuffled, unique list with approximate disorder in 0.01->0.99
    Returns: nums, actual_disorder
    """
    nums = random.sample(range(1, MAX_INT + 1), size)
    nums.sort()
    nums = generate_list_with_target_disorder_fast(nums, target_fraction)
    actual_disorder = compute_disorder(nums)
    # clamp extreme cases
    if actual_disorder <= 0.005 or actual_disorder >= 0.995:
        random.shuffle(nums)
        actual_disorder = compute_disorder(nums)
    return nums, actual_disorder

# --------------------------
# push_swap runner
# --------------------------
def run_pushswap(pushswap, algo, nums):
    cmd = [pushswap]
    if algo is not None:  # Only add flag if algo specified
        cmd.append(f"--{algo}")
    cmd += list(map(str, nums))
    start = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    end = time.perf_counter()
    out = proc.stdout.strip()
    moves = len(out.splitlines())  # Push_swap outputs one instruction per line
    return end - start, moves

# --------------------------
# Benchmarking
# --------------------------

def benchmark(pushswap, algos, size, runs):
    results = defaultdict(lambda: {"moves": [], "disorder": [], "time": []})
    for run in range(runs):
        target_disorder = 0.01 + 0.98 * run / max(1, runs - 1)
        nums, actual_disorder = generate_benchmark_list(size, target_disorder)
        for algo in algos:
            algo_key = "default" if algo is None else algo
            t, m = run_pushswap(pushswap, algo, nums)
            results[algo_key]["moves"].append(m)
            results[algo_key]["disorder"].append(actual_disorder)
            results[algo_key]["time"].append(t)
            print(f"run={run+1}/{runs} algo={algo_key} disorder={actual_disorder:.3f} moves={m} time={t:.4f}s")
    return results

# --------------------------
# CSV saving
# --------------------------

def save_results_csv(results, algo, size):
    """Save results for reproducibility"""
    os.makedirs("data", exist_ok=True)
    filename = f"data/{algo}_n{size}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["disorder", "moves", "time"])
        for d, m, t in zip(results[algo]["disorder"], results[algo]["moves"], results[algo]["time"]):
            writer.writerow([f"{d:.5f}", m, f"{t:.5f}"])
    print(f"Saved raw data: {filename}")


# --------------------------
# CSV Reading and Stats
# --------------------------

def read_results_csv(algo, size):
    """Read CSV and return disorder[], moves[], times[] as lists"""
    filename = f"data/{algo}_n{size}.csv"
    disorders, moves, times = [], [], []
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            disorders.append(float(row["disorder"]))
            moves.append(int(row["moves"]))
            times.append(float(row["time"]))
    return disorders, moves, times

def compute_stats(moves):
    worst = max(moves)
    best = min(moves)
    avg = sum(moves) / len(moves)
    return worst, best, avg

# --------------------------
# Plotting
# --------------------------
def plot_single_from_csv(algo, size):
    """Plot one algorithm from CSV"""
    os.makedirs("plots", exist_ok=True)
    disorders, moves, times = read_results_csv(algo, size)
    worst, best, avg = compute_stats(moves)

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(times, moves, c=disorders, cmap="viridis", alpha=0.8)

    # Labels and title
    ax.set_xlabel("CPU Time (s)")
    ax.set_ylabel("Moves")
    ax.set_title(f"{algo} performance (N={size})")

    # Colorbar
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Disorder")

    # Statistics box

    stats_text = (
        f"Worst moves: {worst}\n"
        f"Best moves:  {best}\n"
        f"Average:     {avg:.2f}"
    )
    fig.tight_layout(rect=[0, 0, 0.80, 1])  # reserve right space
    fig.text(
        0.83,
        0.5,
        stats_text,
        ha="left",
        va="center",
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    ax.grid(True)

    # Save figure
    out_file = f"plots/{algo}_n{size}.png"
    fig.savefig(out_file, bbox_inches="tight")
    plt.close(fig)

    # Print clickable absolute path
    abs_path = os.path.abspath(out_file)
    print(f"Saved plot from CSV: file://{abs_path}")


def plot_compare_from_csv(size):
    """Compare algorithms: CPU time vs moves colored by disorder, different marker per algo"""
    os.makedirs("plots", exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6))

    algo_markers = {
        "simple": "o",
        "medium": "s",
        "complex": "^",
    }

    scatter = None

    # --------------------------
    # Scatter plots
    # --------------------------
    for algo, marker in algo_markers.items():
        filename = f"data/{algo}_n{size}.csv"
        if not os.path.exists(filename):
            print(f"CSV file not found: {filename}, skipping {algo}")
            continue
        disorders, moves, times = read_results_csv(algo, size)
        ax.scatter(times, moves, c=disorders, cmap="viridis",
                   alpha=0.7, marker=marker, edgecolors="k", linewidths=0.3, label=algo)

    # --------------------------
    # Axes labels and title
    # --------------------------
    ax.set_xlabel("CPU Time (s)")
    ax.set_ylabel("Moves")
    ax.set_title(f"Push_swap Algorithm Comparison (N={size})")
    ax.grid(True)

    # --------------------------
    # Colorbar
    # --------------------------
    if scatter is not None:
        cbar = fig.colorbar(scatter, ax=ax)
        cbar.set_label("Disorder")

    # --------------------------
    # Legend
    # --------------------------
    ax.legend(title="Algorithm")

    # --------------------------
    # Statistics per algorithm
    # --------------------------
    stats_lines = []

    for algo in algo_markers.keys():
        filename = f"data/{algo}_n{size}.csv"
        if not os.path.exists(filename):
            continue

        df = pd.read_csv(filename)

        worst = df["moves"].max()
        best = df["moves"].min()
        avg = df["moves"].mean()

        stats_lines.append(
            f"{algo}\n"
            f"  worst: {worst}\n"
            f"  best:  {best}\n"
            f"  avg:   {avg:.2f}"
        )

    stats_text = "\n\n".join(stats_lines)

    # --------------------------
    # Layout: reserve right space
    # --------------------------
    fig.tight_layout(rect=[0, 0, 0.80, 1])

    # --------------------------
    # Statistics box (right side)
    # --------------------------
    fig.text(
        0.83,
        0.5,
        stats_text,
        ha="left",
        va="center",
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9)
    )

    # --------------------------
    # Save figure
    # --------------------------
    out_file = f"plots/compare_n{size}.png"
    fig.savefig(out_file)
    plt.close(fig)
    abs_path = os.path.abspath(out_file)
    print(f"Saved comparison plot from CSV: file://{abs_path}")



def positive_int_greater_one(value):
    ivalue = int(value)
    if ivalue <= 1:
        raise argparse.ArgumentTypeError(f"size must be greater than 1, got {value}")
    return ivalue



def main():
    # --------------------------
    # Handle "clean" as first argument
    # --------------------------
    if len(sys.argv) > 1 and sys.argv[1].lower() == "clean":
        for folder in ["data", "plots"]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"Removed folder: {folder}")
        print("Clean complete.")
        sys.exit(0)

    # --------------------------
    # Configuration
    # --------------------------
    VALID_ALGOS = ["simple", "medium", "complex", "adaptive", "compare"]
    pushswap = None
    algo = None
    size = None
    runs = 200  # default runs

    # --------------------------
    # Parse arguments manually
    # --------------------------
    args = sys.argv[1:]  # exclude script name

    if not args:
        print("Error: missing arguments")
        print("Usage: ./bench <push_swap_path> [size] [algorithm] [runs]")
        sys.exit(1)

    pushswap = args[0]
    rest = args[1:]

    # Identify numeric arguments
    for token in rest[:]:
        if token.isdigit():
            if size is None:
                size = int(token)
            else:
                runs = int(token)
            rest.remove(token)

    # Anything left could be algorithm
    for token in rest:
        if token.lower() in VALID_ALGOS:
            algo = token.lower()
        else:
            print(f"Error: invalid algorithm '{token}'")
            print(f"Choose one of: {', '.join(VALID_ALGOS)}")
            sys.exit(1)

    # --------------------------
    # Validate push_swap
    # --------------------------
    if not os.path.isfile(pushswap) or not os.access(pushswap, os.X_OK):
        print(f"Error: push_swap executable not found or not executable: {pushswap}")
        sys.exit(1)

    # --------------------------
    # Validate size
    # --------------------------
    if size is None or size <= 1:
        print(f"Error: invalid size '{size}', must be integer > 1")
        sys.exit(1)

    if size > MAX_INT:
        print(f"Error: size {size} exceeds MAX_INT={MAX_INT}")
        sys.exit(1)

    # --------------------------
    # Determine algorithms to run
    # --------------------------
    if algo == "compare":
        algos = ["simple", "medium", "complex"]
    else:
        algos = [algo]  # could be None for default

    # --------------------------
    # Run benchmark
    # --------------------------
    results = benchmark(pushswap, algos, size, runs)

    # Save CSV
    for a in algos:
        algo_name = "default" if a is None else a
        save_results_csv(results, algo_name, size)

    # Plot
    if algo == "compare":
        plot_compare_from_csv(size)
    else:
        algo_name = "default" if algo is None else algo
        plot_single_from_csv(algo_name, size)


if __name__ == "__main__":
    main()