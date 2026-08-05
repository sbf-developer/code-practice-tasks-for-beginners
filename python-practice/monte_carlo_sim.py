# ============================================================
# Monte Carlo Simulation — estimate pi
#
# Idea:
#   - Draw random points in a 1x1 square
#   - Count how many fall inside a quarter-circle of radius 1
#   - Area ratio -> estimate of pi
#
# Run: python monte_carlo_pi.py
# ============================================================

import random

def estimate_pi(num_simulations: int 100_000, seed: int = 42) -> float:
    random.seed(seed)

    inside_circle = 0

    for _ in range(num_simulations):
        x = random.random()
        y = random.random()

        if x * x + y * y <= 1:
            inside_circle += 1

    pi_estimate = 4 * inside_circle / num_simulations
    return pi_estimate


def main():
    trials = [1_000, 10_000, 100_000, 1_000_000]

    print("Monte Carlo estimate of pi")
    print("=" * 40)
    print(f"True pi = {3.141592653589793:.15f}")










###### SOLUTION EXAMPLE BELOW --- CAN GIVE BELOW TO CHAT WITH PROMPT "just write this again"




# ============================================================
# Monte Carlo Simulation — estimate pi
#
# Idea:
#   - Draw random points in a 1x1 square
#   - Count how many fall inside a quarter-circle of radius 1
#   - Area ratio -> estimate of pi
#
# Run: python monte_carlo_pi.py
# ============================================================

import random


def estimate_pi(num_simulations: int = 100_000, seed: int = 42) -> float:
    random.seed(seed)

    inside_circle = 0

    for _ in range(num_simulations):
        x = random.random()   # random x between 0 and 1
        y = random.random()   # random y between 0 and 1

        # Point is inside quarter-circle if x^2 + y^2 <= 1
        if x * x + y * y <= 1:
            inside_circle += 1

    # pi/4 = inside / total  ->  pi = 4 * inside / total
    pi_estimate = 4 * inside_circle / num_simulations
    return pi_estimate


def main():
    trials = [1_000, 10_000, 100_000, 1_000_000]

    print("Monte Carlo estimate of pi")
    print("=" * 40)
    print(f"True pi = {3.141592653589793:.15f}")
    print()

    for n in trials:
        estimate = estimate_pi(num_simulations=n)
        error = abs(estimate - 3.141592653589793)
        print(f"Simulations: {n:>8,}")
        print(f"Estimate:    {estimate:.10f}")
        print(f"Error:       {error:.10f}")
        print()


if __name__ == "__main__":
    main()