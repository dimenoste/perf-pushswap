# perf-pushswap

Simple CLI to benchmark a `push_swap` executable.

It generates random sequences, runs `push_swap`, and records:
- number of moves
- execution time

Results are saved as **CSV files and plots**.

---

# 1. IMPORTANT Installation

**1. Go to your push swap folder project**

Example :
```bash
cd <path to push swap project>
make
```

**2. Install inside your push swap folder and run**
```bash
git clone https://github.com/dimenoste/perf-pushswap.git
cd perf-pushswap
cp ../push_swap ./perf-pushswap

./bench ./push_swap 100
```

Requirements:
- Python 3.8+
- Bash

---

# 2. IMPORTANT

1. **go to your push swap project folder** and do:
```bash
make
```
copy the created push_swap executable to perf-pushswap/

2. You must place your compiled **`push_swap` executable** inside this folder.

Result :
```
perf-pushswap/
├── bench
├── src/
├── push_swap   <-- put it here
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
./bench ./push_swap 500 complex 500
```

- algorithm: `complex`
- size: 500
- runs: 500

![Example Plot](plots/complex_n500.png)
---

### Compare all algorithms

```bash
./bench ./push_swap 500 compare 100
```

Runs:
- `simple`
- `medium`
- `complex`

Produces a comparison plot to sort a list of 500 elements, 100 times.

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
