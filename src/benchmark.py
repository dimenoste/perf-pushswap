#!/usr/bin/env python3

import subprocess
import random
import time
import argparse
import os
import csv
import pandas as pd
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
    """Run push_swap and count moves and time"""
    cmd = [pushswap, f"--{algo}"] + list(map(str, nums))
    start = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    end = time.perf_counter()
    moves = len(proc.stdout.strip().splitlines())
    return end - start, moves

# --------------------------
# Benchmarking
# --------------------------

def benchmark(pushswap, algos, size, runs):
    results = defaultdict(lambda: {"moves": [], "disorder": [], "time": []})
    for run in range(runs):
        # Linearly interpolate disorder 0.01 -> 0.99
        target_disorder = 0.01 + 0.98 * run / max(1, runs - 1)
        nums, actual_disorder = generate_benchmark_list(size, target_disorder)
        for algo in algos:
            t, m = run_pushswap(pushswap, algo, nums)
            results[algo]["moves"].append(m)
            results[algo]["disorder"].append(actual_disorder)
            results[algo]["time"].append(t)
            print(f"run={run+1}/{runs} algo={algo} disorder={actual_disorder:.3f} moves={m} time={t:.4f}s")
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
# Plotting
# --------------------------

def plot_single_from_csv(algo, size):
    """Plot one algorithm from CSV"""
    os.makedirs("plots", exist_ok=True)
    filename = f"data/{algo}_n{size}.csv"
    df = pd.read_csv(filename)
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        df["time"],        # x-axis: CPU time
        df["moves"],       # y-axis: moves
        c=df["disorder"],  # color: disorder
        cmap="viridis",
        alpha=0.8
    )
    plt.xlabel("CPU Time (s)")
    plt.ylabel("Moves")
    plt.title(f"{algo} performance (N={size})")
    plt.colorbar(scatter, label="Disorder")
    plt.grid(True)
    out_file = f"plots/{algo}_n{size}.png"
    plt.savefig(out_file)
    plt.close()
    print(f"Saved plot from CSV: {out_file}")


def plot_compare_from_csv(size):
    """Compare algorithms: CPU time vs moves colored by disorder, different marker per algo"""
    os.makedirs("plots", exist_ok=True)
    plt.figure(figsize=(12, 6))

    algo_markers = {
        "simple": "o",
        "medium": "s",
        "complex": "^",
        "adaptive": "D"
    }

    for algo, marker in algo_markers.items():
        filename = f"data/{algo}_n{size}.csv"
        if not os.path.exists(filename):
            print(f"CSV file not found: {filename}, skipping {algo}")
            continue
        df = pd.read_csv(filename)
        plt.scatter(
            df["time"],
            df["moves"],
            c=df["disorder"],
            cmap="viridis",
            alpha=0.7,
            marker=marker,
            edgecolors='k',
            linewidths=0.3,
            label=algo
        )

    plt.xlabel("CPU Time (s)")
    plt.ylabel("Moves")
    plt.title(f"Push_swap Algorithm Comparison (N={size})")
    plt.colorbar(label="Disorder")
    plt.legend(title="Algorithm")
    plt.grid(True)
    plt.tight_layout()
    out_file = f"plots/compare_n{size}.png"
    plt.savefig(out_file)
    plt.close()
    print(f"Saved comparison plot from CSV: {out_file}")



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
    # CLI argument parser
    # --------------------------
    parser = argparse.ArgumentParser(
        description="Benchmark push_swap algorithms and plot results"
    )
    parser.add_argument("pushswap", help="Path to push_swap executable")
    parser.add_argument("algo", help="Algorithm: simple, medium, complex, adaptive, compare")
    parser.add_argument("size", type=positive_int_greater_one, help="Number of integers in the list")
    parser.add_argument("runs", type=positive_int_greater_one, nargs="?", default=200, help="Number of runs per algorithm")
    parser.add_argument("--clean", action="store_true", help="Delete all CSV data and plots")

    args = parser.parse_args()

    # --------------------------
    # Check push_swap executable
    # --------------------------
    if not args.clean:  # only check if we're actually running a benchmark
        if not os.path.isfile(args.pushswap) or not os.access(args.pushswap, os.X_OK):
            print(f"Error: push_swap executable not found or not executable: {args.pushswap}")
            sys.exit(1)

    # --------------------------
    # Enforce required args only if not cleaning
    # --------------------------
    if not args.pushswap or not args.algo or not args.size:
        parser.print_help()
        sys.exit(1)

    # --------------------------
    # Validate size 
    # --------------------------
    if args.size <= 1:
        print(f"Error: size must be positive and greater that 1, got {args.size}")
        sys.exit(1)

    if args.size > MAX_INT:
        print(f"Error: size {args.size} is larger than the maximum allowed {MAX_INT}")
        sys.exit(1)

    # --------------------------
    # Validate algorithm
    # --------------------------
    VALID_ALGOS = ["simple", "medium", "complex", "adaptive", "compare"]
    if args.algo not in VALID_ALGOS:
        print(f"Error: invalid algorithm '{args.algo}'")
        print(f"Choose one of: {', '.join(VALID_ALGOS)}")
        sys.exit(1)
    # --------------------------
    # Determine algorithms to run
    # --------------------------
    if args.algo == "compare":
        algos = ["simple", "medium", "complex", "adaptive"]
    else:
        algos = [args.algo]

    # --------------------------
    # Run benchmark
    # --------------------------
    results = benchmark(args.pushswap, algos, args.size, args.runs)

    # Save CSV for reproducibility
    for algo in algos:
        save_results_csv(results, algo, args.size)

    # Generate plots
    if args.algo == "compare":
        plot_compare_from_csv(args.size)
    else:
        plot_single_from_csv(args.algo, args.size)


if __name__ == "__main__":
    main()