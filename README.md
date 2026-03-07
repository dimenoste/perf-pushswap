# perf-pushswap
## Push_swap Benchmarking Tool

A command-line tool to benchmark different `push_swap` sorting algorithms and visualize their behavior. The tool supports multiple algorithms, adjustable input sizes, multiple runs, and automated plot generation.

---

## Table of Contents

- [Description](#description)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Usage](#usage)  
  - [Help](#help)  
  - [Benchmark Single Algorithm](#benchmark-single-algorithm)  
  - [Compare All Algorithms](#compare-all-algorithms)  
  - [Clean Data and Plots](#clean-data-and-plots)  
- [Output Files](#output-files)  
- [Interpreting Plots](#interpreting-plots)  
- [Notes](#notes)  

---

## Description

`perf-pushswap` allows you to benchmark your `push_swap` executable by generating **random integer sequences** of a given size and measuring:

- Number of **moves** performed  
- Execution **time**  
- Initial **disorder** of the sequence  

It then **saves the raw results in CSV** and **generates plots** showing algorithm performance. This helps to analyze:

- How the algorithm scales with input size  
- Sensitivity to disorder in the input  
- Relative efficiency of multiple algorithms  

---

## Requirements

- Python 3.8+  
- Bash (for `bench` CLI script)  
- `matplotlib` and `pandas` (installed automatically in virtual environment)  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/<username>/cli-perf.git
cd cli-perf
```

2. Usage

Help
```bash
./bench --help
```
Output:
```bash
Usage: ./bench [options] <push_swap_path> <algorithm> <size> [runs]

Arguments / Options:
  <push_swap_path>   Path to your push_swap executable
  <algorithm>        simple | medium | complex | adaptive | compare
  <size>             Number of integers (positive integer)
  [runs]             Optional: number of runs per algorithm (default: 200)
  --clean            Remove all CSVs and plots
  clean              Same as --clean
  ```


  Benchmark Single Algorithm
./bench ./push_swap simple 10 5

Benchmarks the simple algorithm

size=10 integers

runs=5

Example Output:

run=1/5 algo=simple disorder=0.42 moves=12 time=0.0023s
...
Saved raw data: data/simple_n10.csv
Saved plot from CSV: plots/simple_n10.png
Compare All Algorithms
./bench ./push_swap compare 50

Runs all algorithms: simple, medium, complex, adaptive

size=`200`

Default runs=`200` 

Example Output:

Saved raw data: data/simple_n50.csv
Saved raw data: data/medium_n50.csv
Saved raw data: data/complex_n50.csv
Saved raw data: data/adaptive_n50.csv
Saved comparison plot: plots/compare_n50.png

Delete folders data and output

Remove all generated CSV files and plots:

`./bench clean`

Output:

Removed folder: data
Removed folder: plots
Clean complete.
Output Files

Raw data CSVs: data/<algorithm>_n<size>.csv

Plots: plots/<algorithm>_n<size>.png or plots/compare_n<size>.png

File	Description
data/simple_n10.csv	Raw benchmark results for simple algorithm, size 10
plots/simple_n10.png	Plot of moves vs CPU time for simple algorithm
plots/compare_n50.png	Comparison plot of all algorithms for size 50
Interpreting Plots

X-axis: CPU time (seconds)

Y-axis: Number of moves performed

Color: Initial disorder of the sequence (0 = sorted, 1 = fully random)

Insights:

Steeper slopes → algorithm scales poorly with disorder or size

Flat or low slope → algorithm is more efficient

Comparison plots highlight differences between algorithms for the same input size

Example: Adaptive algorithm may show fewer moves and faster execution for nearly sorted sequences compared to simple or medium.

##Notes

push_swap executable must be present and executable. The script checks this automatically.

Algorithm names must be one of: simple, medium, complex, adaptive, compare.

Input size must be a positive integer ≤ MAX_INT (default 1000).

Benchmark runs with unique sequences; adjust MAX_INT in benchmark.py if needed for larger lists.