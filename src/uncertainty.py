"""
uncertainty.py
--------------
Monte Carlo uncertainty analysis for the PET end-of-life pathway model.

Instead of using ONE fixed value per parameter (like model.py does), this
script assigns each parameter a plausible RANGE (min, max), then runs the
model thousands of times, each time picking a random value from within
each range. This tells us:

  1. The spread of possible outcomes for each pathway (not just one number)
  2. How often each pathway "wins" (has the lowest impact) across all runs
  3. Whether the ranking between pathways is stable, or flips depending
     on which assumptions turn out to be true

This directly answers the research question: does the "best" pathway stay
the best under realistic uncertainty, or does it depend on assumptions?
"""

import random
import statistics
from model import (
    mechanical_recycling,
    chemical_recycling,
    energy_recovery,
    landfill,
)

N_SIMULATIONS = 5000  # how many random draws to run


def sample(range_tuple):
    """Pick one random value uniformly between (min, max)."""
    low, high = range_tuple
    return random.uniform(low, high)


# --- Parameter RANGES instead of fixed values ---
# Format: (min, max). These are still rough starting ranges -- refine with
# your own literature sources later. Widen/narrow them as you find better data.

mech_ranges = {
    "collection_rate": (0.60, 0.85),
    "sorting_yield": (0.80, 0.95),
    "process_yield": (0.85, 0.95),
    "rpet_emission_factor": (0.35, 0.60),
    "virgin_emission_factor": (1.90, 2.40),
    "landfill_emission_factor": (0.03, 0.08),
}

chem_ranges = {
    "collection_rate": (0.60, 0.85),
    "process_yield": (0.70, 0.90),
    "chemical_emission_factor": (0.80, 1.80),
    "virgin_emission_factor": (1.90, 2.40),
    "landfill_emission_factor": (0.03, 0.08),
}

energy_ranges = {
    "combustion_emission_factor": (2.0, 3.0),
    "energy_recovered_per_kg": (15, 25),
    "grid_emission_factor": (0.05, 0.15),
}

landfill_ranges = {
    "landfill_emission_factor": (0.03, 0.08),
}


def run_simulation():
    """Run N_SIMULATIONS random draws for all 4 pathways."""
    results = {
        "Mechanical Recycling": [],
        "Chemical Recycling": [],
        "Energy Recovery": [],
        "Landfill": [],
    }

    win_counts = {name: 0 for name in results}

    for _ in range(N_SIMULATIONS):
        mech_params = {k: sample(v) for k, v in mech_ranges.items()}
        chem_params = {k: sample(v) for k, v in chem_ranges.items()}
        energy_params = {k: sample(v) for k, v in energy_ranges.items()}
        landfill_params = {k: sample(v) for k, v in landfill_ranges.items()}

        run_results = {
            "Mechanical Recycling": mechanical_recycling(mech_params),
            "Chemical Recycling": chemical_recycling(chem_params),
            "Energy Recovery": energy_recovery(energy_params),
            "Landfill": landfill(landfill_params),
        }

        for name, value in run_results.items():
            results[name].append(value)

        # find the winner (lowest impact) for this single run
        winner = min(run_results, key=run_results.get)
        win_counts[winner] += 1

    return results, win_counts


def summarize(results, win_counts, n_simulations):
    print(f"Monte Carlo results over {n_simulations} simulations\n")
    print(f"{'Pathway':<22}{'Mean':>10}{'Std Dev':>10}{'Min':>10}{'Max':>10}{'Win %':>10}")
    print("-" * 72)

    for name, values in results.items():
        mean = statistics.mean(values)
        stdev = statistics.stdev(values)
        vmin = min(values)
        vmax = max(values)
        win_pct = 100 * win_counts[name] / n_simulations
        print(f"{name:<22}{mean:>10.1f}{stdev:>10.1f}{vmin:>10.1f}{vmax:>10.1f}{win_pct:>9.1f}%")


if __name__ == "__main__":
    results, win_counts = run_simulation()
    summarize(results, win_counts, N_SIMULATIONS)
