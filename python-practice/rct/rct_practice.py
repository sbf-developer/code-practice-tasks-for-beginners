# ============================================================
# Randomized Controlled Trial (RCT) — practice
# Write your solution below each task comment.
#
# Stuck? Write pseudocode first — plain-English steps of what your
# program should do. Once the logic makes sense, translate it into code.
#
# Data file: trial_data.csv (same as in rct_solution.py)
# See rct_solution.py for a worked example.
# ============================================================

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable



# 0. Trial design 

TRIAL_NAME = "Job Training RCT"
PRIMARY_OUTCOME = "post_income"
BASELINE_COVARIATES = ["age", "female", "baseline_income", "baseline_score"]
RANDOMIZATION_RATIO = (1, 1)  # treated : control
ALPHA = 0.05
HYPOTHESIS = "Job training raises post-program income relative to control."

DATA_FILE = Path(__file__).parent / "trial_data.csv"



# 1. Load trial data 

def load_trial_data() -> list[dict]:
    """
    Load finalized participant records from the cleaned data export.

    In a real project this file comes from your data team after collection,
    cleaning, and de-identification. The analysis code never constructs outcomes.
    """
    rows: list[dict] = []

    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        for record in csv.DictReader(f):
            post = record[PRIMARY_OUTCOME].strip()
            rows.append(
                {
                    "id": int(record["id"]),
                    "age": float(record["age"]),
                    "female": int(record["female"]),
                    "baseline_income": float(record["baseline_income"]),
                    "baseline_score": float(record["baseline_score"]),
                    "treat": int(record["treat"]),
                    PRIMARY_OUTCOME: float(post) if post else None,
                }
            )

    return rows

    # 2. Statistics helpers

    def mean(values: Iterable[float]) -> float:
        vals = list(values)
        return sum(vals) / len(vals)


    def variance(values: Iterable[float], ddof: int = 1) -> float:
        vals = list(values)
        if len(vals) <= ddof:
            return float("nan")
        m = mean(vals)
        return math.sqrt(variance(values, ddof=ddof))

    def std_dev(values: Iterable[float], ddof: int = 1) -> float:
        return math.sqrt(variance(values, ddof=ddof))

    def normal_cdf(x: float) -> float:
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    def two_sided_p_from_z(z: float) -> float:
        return 2.0 (1.0 - normal_cdf(abs(z)))

    
    @dataclass
    class TwoSampleResult:
        n_t: int
        n_c: int
        mean_t: float
        mean_c: float
        diff: float
        se: float
        ci_low: float
        ci_high: float
        t_stat: float
        p_value: float
        cohens_d: float

    def welch_two_samples(values_t: list[float], values_c: list[float]) -> TwoSampleResult:
        """Welch's unequal-variance two-sample comparison."""
        n1, n0 = len(values_t), len(values_c)
        m1, m0 = mean(values_t), mean(values_c)
        v1, v0 = variance(values_t), variance(values_c)

        diff = m1 - m0
        se = math.sqrt(v1 / n1 + v0 / n0)
        t_stat = diff / se if se > 0 else float("inf")
        p_value = two_sided_p_from_z(t_stat)

        z_crit = 1.96
        ci_low = diff - z_crit * se
        ci_high = diff + z_crit * se

        pooled_sd = math.sqrt(((n1 - 1) * v1 + (n0 - 1) * v0) / (n1 + n0 - 2))
        cohens_d = diff / pooled_sd if pooled_sd > 0 else float("nan")
        
