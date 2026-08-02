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
