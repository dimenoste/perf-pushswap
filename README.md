# perf-pushswap
## Push_swap Benchmarking Tool

A command-line tool to benchmark different `push_swap` sorting algorithms and visualize their behavior. Supports multiple algorithms, adjustable input sizes, multiple runs, and automatic plot generation.
Make sure you have a correct running push-swap executable.
---

## Description

The CLI is a helper to help diagnose, share and reproduce results obtained in the context of the 42 school project Push-swap. 
The goal of Push-Swap is to sort one sequence of number using two stacks
`perf-pushswap` benchmarks your `push_swap` executable by generating **random integer sequences** and measuring:

- Number of **moves** performed  
- Execution **time**  
- Initial **disorder** of the sequence
Across multiple runs.

Results are saved as CSV and plots for easy comparison and further research.

---

## Requirements

- Python 3.8+  
- Bash (for `bench` CLI)  
- `matplotlib` and `pandas` (installed automatically in venv)  

---

## Installation

```bash
git clone https://github.com/dimenoste/perf-pushswap.git 
cd perf-pushswap
chmod +x bench src/benchmark.py  # optional, Git preserves executable bit
```
BEFORE ANYTHING Move your **push-swap executable inside perf-pushwap** !

```bash
./bench ./push_swap 10
```

---

## Usage

### Help

```bash
./bench --help
```

**Output:**
```
Usage: ./bench <push_swap_path> [size] [algorithm] [runs]

Arguments / Options:
  <push_swap_path>   Path to your push_swap executable
  [size]             Number of integers to sort (positive integer > 1)
  [algorithm]        Optional/ Relevant for new 42 project: simple | medium | complex | adaptive | compare
                     If omitted, the project may choose the algorithm internally
  [runs]             Optional number of runs (default: 200)
  clean              Remove all CSVs and plots
```

---

### Benchmark Single Algorithm

```bash
./bench ./push_swap 10
```

- Benchmarks your default algorithm (it should be adaptive as specified in the 2025 42 subject)
- sort 10 integers, 200 runs  

**Example Output:**
```bash
run=1/5 algo=default disorder=0.42 moves=12 time=0.0023s

Saved raw data: data/default_n10.csv
Saved plot from CSV: plots/default_n10.png
```

### Specify the algorithm complexity as per new subject of pushswap (2025)

```bash
./bench ./push_swap 500 medium 100
```
Benchmarks `medium` algorithm
500 integers, 100 runs

### Compare All Algorithms (only for new 2025 project)

```bash
./bench ./push_swap 500 compare 500
```
- Runs: `simple`, `medium`, `complex` 
- Size = 500, runs = 500  

**Example Output:**
```
Saved raw data: data/simple_n500.csv
Saved raw data: data/medium_n500.csv
Saved raw data: data/complex_n500.csv
Saved comparison plot: plots/compare_n500.png
```

**Example Plot:**

![Example Plot](plots/complex_n500.png)

porduced by the benchmark for a `complex` algo (new subject as of 2026)
```bash
./bench ./push_swap 500 complex
``` 
---

### Clean Data and Plots

```bash
./bench clean
```

**Output:**
```
Removed folder: data
Removed folder: plots
Clean complete.
```

---

## Output Files

| File | Description |
|------|-------------|
| `data/<algorithm>_n<size>.csv` | Raw benchmark results |
| `plots/<algorithm>_n<size>.png` | Plot of moves vs CPU time for a single algorithm |
| `plots/compare_n<size>.png` | Comparison plot of all algorithms |

---

## Interpreting Plots

- **X-axis:** CPU time (seconds)  
- **Y-axis:** Number of moves  
- **Color:** Initial disorder (0 = sorted, 1 = random)  

**Insights:**

- Steep slope → scales poorly with disorder/size  
- Flat slope → more efficient  
- Comparison plots show relative efficiency of multiple algorithms  
- Example: `adaptive` often uses fewer moves on nearly sorted sequences.

---

## Notes

- `push_swap` executable must exist and be executable.  
- Algorithms (relevant for new 2025 project) : `simple`, `medium`, `complex`, `adaptive`, `compare`  
- `size` must be a positive integer > 1 and ≤ `MAX_INT` (default 1000)  
- Each run uses a unique sequence with a disorder from 0.01 to 0.99. Run value must be greater than 2.
