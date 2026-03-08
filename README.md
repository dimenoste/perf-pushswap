# perf-pushswap

Simple CLI to benchmark a `push_swap` executable.

It generates random sequences, runs `push_swap`, and records:
- number of moves
- execution time

Results are saved as **CSV files and plots**.

---

# 1. Installation

```bash
git clone https://github.com/dimenoste/perf-pushswap.git
cd perf-pushswap
```

Requirements:
- Python 3.8+
- Bash

---

# 2. IMPORTANT

You must place your compiled **`push_swap` executable** inside this folder.

Example:

```
perf-pushswap/
├── bench
├── src/
├── push_swap   <-- put it here
```

Example compilation:

```bash
make
cp ../push_swap ./push_swap
```

---

# 3. Quick Start

Run a benchmark:

```bash
./bench ./push_swap 100
```

This runs **200 tests** sorting **100 numbers**.

Results are saved in:

```
data/
plots/
```

---

# 4. Basic Usage

```
./bench <push_swap_path> [size] [algorithm] [runs]
```

Arguments:

```
<push_swap_path>   path to push_swap executable
[size]             number of integers (>1)
[algorithm]        simple | medium | complex | adaptive | compare
[runs]             number of runs (default 200)
```

---

# 5. Examples

### Default benchmark

```bash
./bench ./push_swap 100
```

100 numbers, 200 runs.

---

### Benchmark specific algorithm (new 42 subject)

```bash
./bench ./push_swap 500 medium 100
```

- algorithm: `medium`
- size: 500
- runs: 100

---

### Compare all algorithms

```bash
./bench ./push_swap 500 compare 500
```

Runs:
- `simple`
- `medium`
- `complex`

Produces a comparison plot.

---

# 6. Clean generated data

```bash
./bench clean
```

Removes:

```
data/
plots/
```

---

# 7. Output files

```
data/<algorithm>_n<size>.csv
```

Raw benchmark data.

```
plots/<algorithm>_n<size>.png
```

Plot for a single algorithm.

```
plots/compare_n<size>.png
```

Comparison plot between algorithms.

---

# Notes

- `push_swap` must be executable.
- `size` must be >1 and ≤1000.
- `runs` must be >2.
- Algorithms (new subject):  
  `simple`, `medium`, `complex`, `adaptive`.
