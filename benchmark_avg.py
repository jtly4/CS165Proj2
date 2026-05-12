import csv
import os
from collections import defaultdict

# ── Configuration ─────────────────────────────────────────────────────────────

INPUT_DIR  = "."   # where the raw {algorithm_name}.csv files live
OUTPUT_DIR = "."   # where the {algorithm_name}_avg.csv files will be written

ALGORITHMS = [
    "next_fit",
    "first_fit",
    "first_fit_decreasing",
    "best_fit",
    "best_fit_decreasing",
]

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for algo_name in ALGORITHMS:
        input_path  = os.path.join(INPUT_DIR,  f"{algo_name}.csv")
        output_path = os.path.join(OUTPUT_DIR, f"{algo_name}_avg.csv")

        # Collect all trial times and wastes grouped by size
        times_by_size = defaultdict(list)
        waste_by_size = defaultdict(list)

        with open(input_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                size    = int(row["size"])
                time_ns = int(row["time_ns"])
                waste   = float(row["waste"])
                times_by_size[size].append(time_ns)
                waste_by_size[size].append(waste)

        # Write averaged results, sorted by size
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["size", "avg_time_ns", "avg_waste"])

            for size in sorted(times_by_size):
                avg_time  = sum(times_by_size[size]) / len(times_by_size[size])
                avg_waste = sum(waste_by_size[size])  / len(waste_by_size[size])
                writer.writerow([size, avg_time, avg_waste])
                print(f"{algo_name} | size {size:>7} | avg time: {avg_time:.2f} ns | avg waste: {avg_waste:.4f}")

        print(f"  ✓ Saved {output_path}\n")

    print("All averages complete.")


if __name__ == "__main__":
    main()