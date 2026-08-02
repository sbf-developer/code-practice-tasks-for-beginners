# ============================================================
# Randomized Controlled Trial (RCT) — practice
# Write your solution below each task comment.
# Disclaimer: This is a practice RCT with mock data.
#
# Stuck? Write pseudocode first — plain-English steps of what your
# program should do. Once the logic makes sense, translate it into code.
#
# See rct_solution.py for a worked example.
# ============================================================


# Dependencies

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterable


# Trial design

TRIAL_NAME = "Mock Job Training RCT"
PRIMARY_OUTCOME = "post_income"
BASELINE_COVARIATES = ["age", "female", "baseline_income", "baseline_score"]
RANDOMIZATION_RATIO = (1,1) # treated : control
ALPHA = 0.05
HYPOTHESIS = "Job training raises post-program income relative to control."


# Load trial data

def load_trial_data() -> list[dict]:
    """
    Return finalized participant records for analysis.

    In a real project this would read a CSV / database export after
    data collection. Here we generate a realistic mock dataset once.
    The analysis code below treats these rows like observed data only.
    """
    return _generate_mock_records(seed=42, n=400, attrition_rate=0.08)


def _generate_mock_records(seed: int, n: int, attrition_rate: float) -> list[dict]:
    """
    Internal mock data collection — not part of the analysis plan.

    Creates a plausible job-training trial: baseline survey fields,
    random assignment, follow-up income, and some survey nonresponse.
    """
    rng = random.Random(seed)
    rows: list[dict] = []

    for i in range(n):
        age = rng.gauss(35, 10)
        female = 1 if rng.random < 0.52 else 0
        