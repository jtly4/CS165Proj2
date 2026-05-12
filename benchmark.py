import random
import time
import csv
import os

from next_fit import next_fit
from first_fit import first_fit
from first_fit import first_fit_decreasing
from best_fit import best_fit
from best_fit import best_fit_decreasing
from zipzip_tree import ZipZipTree, Rank

# ── Configuration ────────────────────────────────────────────────────────────

# Edit these sizes however you like (e.g. [2**k for k in range(1, 21)] goes up to 2^20)
#SIZES = [2**k for k in range(1, 21)]
'''
2 ** 10 = 1024
2 ** 13 = 8192
2 ** 15 = 32678
2 ** 17 = 131072
2 ** 20 = 1048576
'''
SIZES = [500, 1024, 2500, 5000, 8192, 32678, 131072, 1048576]

TRIALS = 10          # number of random lists per (algorithm, size)
ITEM_MAX = 0.65      # items are drawn uniformly from [0.0, ITEM_MAX]
BIN_CAPACITY = 1.0   # passed to algorithms that need it (unused by waste calc)
OUTPUT_DIR = "."     # where the .csv files are written

# ── Algorithms under test ─────────────────────────────────────────────────────

ALGORITHMS = [
    ("next_fit",             next_fit),
    ("first_fit",            first_fit),
    ("first_fit_decreasing", first_fit_decreasing),
    ("best_fit",             best_fit),
    ("best_fit_decreasing",  best_fit_decreasing),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
 
def random_items(n: int) -> list[float]:
    """Return n floats drawn uniformly from [0.0, 0.65]."""
    return [random.uniform(0.0, ITEM_MAX) for _ in range(n)]
 
 
def run_trial(algorithm, items: list[float]) -> tuple[int, float]:
    """
    Time a single algorithm call and return (elapsed_ns, waste).
    Waste = bins used - sum of items.
    Builds the required `assignments` and `free_space` lists fresh each call.
    """
    assignments = [0] * len(items)
    free_space = []
 
    start = time.perf_counter_ns()
    algorithm(items, assignments, free_space)
    end = time.perf_counter_ns()
 
    elapsed_ns = end - start
    bins_used = len(set(assignments))
    waste = bins_used - sum(items)
    return elapsed_ns, waste
 
# ── Main ──────────────────────────────────────────────────────────────────────
 
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
 
    # Open all CSV writers up front so we can write one row per algorithm per trial
    csv_files = {}
    writers = {}
    for algo_name, _ in ALGORITHMS:
        csv_path = os.path.join(OUTPUT_DIR, f"{algo_name}.csv")
        f = open(csv_path, "w", newline="")
        writer = csv.writer(f)
        writer.writerow(["size", "time_ns", "waste"])
        csv_files[algo_name] = f
        writers[algo_name] = writer
 
    for n in SIZES:
        for trial in range(1, TRIALS + 1):
            items = random_items(n)   # same list for every algorithm this trial
            print(f"Size {n} | Test {trial}")
 
            for algo_name, algo_fn in ALGORITHMS:
                elapsed_ns, waste = run_trial(algo_fn, items.copy())
                writers[algo_name].writerow([n, elapsed_ns, waste])
                print(f"  {algo_name}: {elapsed_ns} ns | waste: {waste:.4f}")
 
            print()
 
    for f in csv_files.values():
        f.close()
 
    print("All benchmarks complete.")
 
 
if __name__ == "__main__":
    main()