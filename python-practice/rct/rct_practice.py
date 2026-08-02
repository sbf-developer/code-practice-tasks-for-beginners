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


# ---------------------------------------------------------------------------
# 0. Trial design (pre-analysis plan — known before seeing outcomes)
# ---------------------------------------------------------------------------
TRIAL_NAME = "Job Training RCT"
PRIMARY_OUTCOME = "post_income"
BASELINE_COVARIATES = ["age", "female", "baseline_income", "baseline_score"]
RANDOMIZATION_RATIO = (1, 1)  # treated : control
ALPHA = 0.05
HYPOTHESIS = "Job training raises post-program income relative to control."

DATA_FILE = Path(__file__).parent / "trial_data.csv"


# ---------------------------------------------------------------------------
# 1. Load trial data (cleaned analysis dataset)
# ---------------------------------------------------------------------------
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