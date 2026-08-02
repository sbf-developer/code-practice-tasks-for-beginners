# ============================================================
# Randomized Controlled Trial (RCT) — academic-style template
#
# One-file workflow using mock trial data that is analyzed the same
# way as a real study: the analyst sees only cleaned participant
# records (assignment, baseline covariates, outcomes).
#
# Pipeline:
#   study setup -> load data -> CONSORT counts -> Table 1 balance ->
#   primary ITT estimate -> covariate-adjusted ANCOVA -> summary
#
# Estimand (primary): Intention-to-Treat (ITT) Average Treatment Effect
#   ITT-ATE = E[Y(1) - Y(0)] among all randomized units,
#   respecting assigned arm regardless of compliance.
#
# Identification: individual-level random assignment (1:1).
#   Assumes SUTVA (no spillovers; one version of treatment).
#   Balance checks are diagnostic only.
#
# Run:  python rct_solution.py
#
# Dependencies: Python standard library only.
# ============================================================

from __future__ import annotations

import math
import random
from dataclasses import dataclass
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


# ---------------------------------------------------------------------------
# 1. Load trial data (mock stand-in for a cleaned analysis dataset)
# ---------------------------------------------------------------------------
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
        female = 1 if rng.random() < 0.52 else 0
        baseline_income = max(12000, rng.gauss(28000, 7000))
        baseline_score = rng.gauss(65, 12)

        # Outcome model unknown to analyst; treatment shifts earnings upward.
        control_outcome = (
            18000
            + 450 * baseline_score
            + 0.35 * baseline_income
            + 120 * female
            + rng.gauss(0, 2500)
        )
        treatment_lift = 2500 + rng.gauss(0, 1200)
        treated_outcome = control_outcome + treatment_lift

        assigned_treatment = 1 if rng.random() < 0.5 else 0
        realized_outcome = treated_outcome if assigned_treatment == 1 else control_outcome

        # Some participants missing at follow-up (handled in CONSORT table).
        post_income = realized_outcome if rng.random() > attrition_rate else None

        rows.append(
            {
                "id": i + 1,
                "age": age,
                "female": female,
                "baseline_income": baseline_income,
                "baseline_score": baseline_score,
                "treat": assigned_treatment,
                "post_income": post_income,
            }
        )

    return rows


# ---------------------------------------------------------------------------
# 2. Statistics helpers
# ---------------------------------------------------------------------------
def mean(values: Iterable[float]) -> float:
    vals = list(values)
    return sum(vals) / len(vals)


def variance(values: Iterable[float], ddof: int = 1) -> float:
    vals = list(values)
    if len(vals) <= ddof:
        return float("nan")
    m = mean(vals)
    return sum((v - m) ** 2 for v in vals) / (len(vals) - ddof)


def std_dev(values: Iterable[float], ddof: int = 1) -> float:
    return math.sqrt(variance(values, ddof=ddof))


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def two_sided_p_from_z(z: float) -> float:
    return 2.0 * (1.0 - normal_cdf(abs(z)))


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


def welch_two_sample(values_t: list[float], values_c: list[float]) -> TwoSampleResult:
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

    return TwoSampleResult(
        n_t=n1,
        n_c=n0,
        mean_t=m1,
        mean_c=m0,
        diff=diff,
        se=se,
        ci_low=ci_low,
        ci_high=ci_high,
        t_stat=t_stat,
        p_value=p_value,
        cohens_d=cohens_d,
    )


def standardized_mean_difference(values_t: list[float], values_c: list[float]) -> float:
    m1, m0 = mean(values_t), mean(values_c)
    s1, s0 = std_dev(values_t), std_dev(values_c)
    pooled = math.sqrt((s1**2 + s0**2) / 2.0)
    return (m1 - m0) / pooled if pooled > 0 else float("nan")


# ---------------------------------------------------------------------------
# 3. OLS for covariate-adjusted ITT (ANCOVA-style)
# ---------------------------------------------------------------------------
def mat_transpose(m: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*m)]


def mat_mul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    rows, cols, inner = len(a), len(b[0]), len(b)
    out = [[0.0] * cols for _ in range(rows)]
    for i in range(rows):
        for k in range(inner):
            for j in range(cols):
                out[i][j] += a[i][k] * b[k][j]
    return out


def mat_vec_mul(a: list[list[float]], v: list[float]) -> list[float]:
    return [sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a))]


def invert_matrix(m: list[list[float]]) -> list[list[float]]:
    n = len(m)
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(m)]
    for col in range(n):
        pivot = aug[col][col]
        if abs(pivot) < 1e-12:
            raise ValueError("Singular matrix in OLS.")
        aug[col] = [x / pivot for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def xt_y(x: list[list[float]], y: list[float]) -> list[float]:
    k = len(x[0])
    return [sum(x[i][j] * y[i] for i in range(len(y))) for j in range(k)]


def ols_with_se(
    y: list[float],
    x: list[list[float]],
    coef_names: list[str],
) -> dict[str, float | dict[str, float]]:
    xtx = mat_mul(mat_transpose(x), x)
    xtx_inv = invert_matrix(xtx)
    beta = mat_vec_mul(xtx_inv, xt_y(x, y))

    n, k = len(y), len(coef_names)
    fitted = mat_vec_mul(x, beta)
    residuals = [y_i - f_i for y_i, f_i in zip(y, fitted)]
    sigma2 = sum(r**2 for r in residuals) / (n - k)
    cov = [[sigma2 * xtx_inv[i][j] for j in range(k)] for i in range(k)]
    se = [math.sqrt(cov[i][i]) for i in range(k)]

    return {
        "names": coef_names,
        "beta": {name: beta[i] for i, name in enumerate(coef_names)},
        "se": {name: se[i] for i, name in enumerate(coef_names)},
        "n": n,
    }


# ---------------------------------------------------------------------------
# 4. Analysis and reporting
# ---------------------------------------------------------------------------
def split_arms(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    treated = [r for r in rows if r["treat"] == 1]
    control = [r for r in rows if r["treat"] == 0]
    return treated, control


def complete_cases(rows: list[dict], outcome: str) -> list[dict]:
    return [r for r in rows if r[outcome] is not None]


def print_study_header() -> None:
    print("=" * 72)
    print(TRIAL_NAME)
    print("=" * 72)
    print(f"Primary estimand: ITT average treatment effect on {PRIMARY_OUTCOME}")
    print(f"Primary hypothesis: {HYPOTHESIS}")
    print(f"Randomization: individual-level {RANDOMIZATION_RATIO[0]}:{RANDOMIZATION_RATIO[1]}")
    print(f"Two-sided significance level: alpha = {ALPHA}")
    print()


def print_consort(rows: list[dict], outcome: str) -> None:
    treated, control = split_arms(rows)
    analyzed = complete_cases(rows, outcome)
    analyzed_t = [r for r in analyzed if r["treat"] == 1]
    analyzed_c = [r for r in analyzed if r["treat"] == 0]

    print("=" * 72)
    print("CONSORT-style participant flow")
    print("=" * 72)
    print(f"Randomized total:                {len(rows):4d}")
    print(f"  Assigned to treatment:         {len(treated):4d}")
    print(f"  Assigned to control:           {len(control):4d}")
    print(f"Missing primary outcome:         {len(rows) - len(analyzed):4d}")
    print(f"Analyzed (complete-case ITT):    {len(analyzed):4d}")
    print(f"  Treatment arm analyzed:        {len(analyzed_t):4d}")
    print(f"  Control arm analyzed:          {len(analyzed_c):4d}")
    print()


def print_table1(rows: list[dict], covariates: list[str]) -> None:
    treated, control = split_arms(rows)
    print("=" * 72)
    print("Table 1. Baseline characteristics by randomized arm")
    print("=" * 72)
    print(f"{'Variable':<22}{'Treat mean (SD)':>18}{'Control mean (SD)':>20}{'Diff':>10}{'SMD':>8}{'p-value':>10}")
    print("-" * 72)

    for var in covariates:
        t_vals = [r[var] for r in treated]
        c_vals = [r[var] for r in control]
        res = welch_two_sample(t_vals, c_vals)
        smd = standardized_mean_difference(t_vals, c_vals)
        print(
            f"{var:<22}"
            f"{res.mean_t:8.2f} ({std_dev(t_vals):5.2f})"
            f"{res.mean_c:10.2f} ({std_dev(c_vals):5.2f})"
            f"{res.diff:10.2f}"
            f"{smd:8.3f}"
            f"{res.p_value:10.4f}"
        )
    print("Note: Large p-values and small SMDs are expected under successful randomization.")
    print()


def print_primary_itt(rows: list[dict], outcome: str) -> TwoSampleResult:
    analyzed = complete_cases(rows, outcome)
    t_vals = [r[outcome] for r in analyzed if r["treat"] == 1]
    c_vals = [r[outcome] for r in analyzed if r["treat"] == 0]
    res = welch_two_sample(t_vals, c_vals)

    print("=" * 72)
    print("Table 2. Primary outcome - ITT difference in means (unadjusted)")
    print("=" * 72)
    print(f"Outcome: {outcome}")
    print(f"Treatment mean (SD): {res.mean_t:,.2f} ({std_dev(t_vals):,.2f}), n = {res.n_t}")
    print(f"Control mean (SD):   {res.mean_c:,.2f} ({std_dev(c_vals):,.2f}), n = {res.n_c}")
    print(f"ITT effect (T - C):  {res.diff:,.2f}")
    print(f"SE:                  {res.se:,.2f}")
    print(f"95% CI:              [{res.ci_low:,.2f}, {res.ci_high:,.2f}]")
    print(f"t-statistic:         {res.t_stat:,.3f}")
    print(f"p-value (two-sided): {res.p_value:,.4f}")
    print(f"Cohen's d:           {res.cohens_d:,.3f}")
    significant = "Yes" if res.p_value < ALPHA else "No"
    print(f"Significant at alpha={ALPHA}: {significant}")
    print()
    return res


def print_adjusted_itt(rows: list[dict], outcome: str) -> None:
    analyzed = complete_cases(rows, outcome)
    y = [r[outcome] for r in analyzed]

    x = []
    for r in analyzed:
        x.append(
            [
                1.0,
                float(r["treat"]),
                r["baseline_score"],
                r["baseline_income"],
                r["age"],
                float(r["female"]),
            ]
        )
    names = [
        "intercept",
        "treat",
        "baseline_score",
        "baseline_income",
        "age",
        "female",
    ]

    fit = ols_with_se(y, x, names)
    b = fit["beta"]["treat"]
    se = fit["se"]["treat"]
    ci_low = b - 1.96 * se
    ci_high = b + 1.96 * se
    z = b / se if se > 0 else float("inf")
    p = two_sided_p_from_z(z)

    print("=" * 72)
    print("Table 3. Adjusted ITT (ANCOVA-style OLS)")
    print("=" * 72)
    print("Model: post_income ~ treat + baseline_score + baseline_income + age + female")
    print(f"Adjusted ITT effect (treat): {b:,.2f}")
    print(f"SE:                        {se:,.2f}")
    print(f"95% CI:                    [{ci_low:,.2f}, {ci_high:,.2f}]")
    print(f"p-value (two-sided):       {p:,.4f}")
    print()


def print_conclusions(primary: TwoSampleResult) -> None:
    print("=" * 72)
    print("Conclusions")
    print("=" * 72)
    direction = "increase" if primary.diff > 0 else "decrease"
    print(
        f"Assigned job training is associated with an estimated {direction} of "
        f"{abs(primary.diff):,.0f} USD in {PRIMARY_OUTCOME} "
        f"(95% CI: {primary.ci_low:,.0f} to {primary.ci_high:,.0f})."
    )
    if primary.p_value < ALPHA:
        print(f"This contrast is statistically significant at alpha = {ALPHA}.")
    else:
        print(f"This contrast is not statistically significant at alpha = {ALPHA}.")
    print()
    print("Limitations noted in this template:")
    print("  - Complete-case analysis; sensitivity to attrition not shown")
    print("  - No clustering adjustment (individual-level randomization assumed)")
    print("  - External validity depends on study population and setting")


# ---------------------------------------------------------------------------
# 5. Main analysis pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    print_study_header()

    data = load_trial_data()

    print_consort(data, PRIMARY_OUTCOME)
    print_table1(data, BASELINE_COVARIATES)
    primary = print_primary_itt(data, PRIMARY_OUTCOME)
    print_adjusted_itt(data, PRIMARY_OUTCOME)
    print_conclusions(primary)


if __name__ == "__main__":
    main()
