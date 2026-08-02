# ============================================================
# Randomized Controlled Trial (RCT) — academic-style template
#
# ILLUSTRATIVE / PEDAGOGICAL: one-file mock trial with known truth.
# Mirrors common reporting in applied papers / trial memos:
#   study setup -> CONSORT counts -> Table 1 balance ->
#   primary ITT estimate -> covariate-adjusted ANCOVA -> summary
#
# Estimand (primary): Intention-to-Treat (ITT) Average Treatment Effect
#   ITT-ATE = E[Y(1) - Y(0)] among all randomized units,
#   respecting assigned arm regardless of compliance.
#
# Identification: individual-level random assignment (1:1).
#   Assumes SUTVA (no spillovers; one version of treatment) and
#   stable randomization. Balance checks are diagnostic only.
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
# 0. Trial design (as in a pre-analysis plan)
# ---------------------------------------------------------------------------
TRIAL_NAME = "Mock Job Training RCT"
PRIMARY_OUTCOME = "post_income"
BASELINE_COVARIATES = ["age", "female", "baseline_income", "baseline_score"]
RANDOMIZATION_RATIO = (1, 1)  # treated : control
ALPHA = 0.05
TRUE_ATE = 2500.0  # planted treatment effect (USD); known in simulation only

RNG = random.Random(42)


# ---------------------------------------------------------------------------
# 1. Mock data generation
# ---------------------------------------------------------------------------
def generate_mock_trial(
    n: int = 400,
    attrition_rate: float = 0.08,
    true_ate: float = TRUE_ATE,
) -> list[dict]:
    """
    Simulate a two-arm individual-level RCT.

    Data-generating process (simulation truth only):
      baseline covariates -> potential outcomes Y(0), Y(1)
      random assignment -> observed outcome under assigned arm
      random attrition after outcome realized (missing at random here)
    """
    rows: list[dict] = []

    for i in range(n):
        age = RNG.gauss(35, 10)
        female = 1 if RNG.random() < 0.52 else 0
        baseline_income = max(12000, RNG.gauss(28000, 7000))
        baseline_score = RNG.gauss(65, 12)

        # Potential outcomes: treatment adds true_ate on average.
        y0 = (
            18000
            + 450 * baseline_score
            + 0.35 * baseline_income
            + 120 * female
            + RNG.gauss(0, 2500)
        )
        y1 = y0 + true_ate + RNG.gauss(0, 1200)

        treat = 1 if RNG.random() < 0.5 else 0
        observed = y1 if treat == 1 else y0

        # Post-randomization attrition (unrelated to potential outcomes here).
        observed_outcome = observed if RNG.random() > attrition_rate else None

        rows.append(
            {
                "id": i + 1,
                "age": age,
                "female": female,
                "baseline_income": baseline_income,
                "baseline_score": baseline_score,
                "treat": treat,
                "post_income": observed_outcome,
            }
        )

    return rows


# ---------------------------------------------------------------------------
# 2. Statistics helpers (stdlib implementations)
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
    """Welch's unequal-variance two-sample comparison (common in RCT papers)."""
    n1, n0 = len(values_t), len(values_c)
    m1, m0 = mean(values_t), mean(values_c)
    v1, v0 = variance(values_t), variance(values_c)

    diff = m1 - m0
    se = math.sqrt(v1 / n1 + v0 / n0)

    # Welch-Satterthwaite degrees of freedom.
    num = (v1 / n1 + v0 / n0) ** 2
    den = (v1 / n1) ** 2 / (n1 - 1) + (v0 / n0) ** 2 / (n0 - 1)
    df = num / den if den > 0 else min(n1, n0) - 1

    t_stat = diff / se if se > 0 else float("inf")
    # Normal approximation for p-value (adequate at moderate/large n).
    p_value = two_sided_p_from_z(t_stat)

    z_crit = 1.96  # large-sample 95% CI (common in applied reporting).
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
    """SMD used in balance tables; |SMD| < 0.1 often called negligible."""
    m1, m0 = mean(values_t), mean(values_c)
    s1, s0 = std_dev(values_t), std_dev(values_c)
    pooled = math.sqrt((s1**2 + s0**2) / 2.0)
    return (m1 - m0) / pooled if pooled > 0 else float("nan")


# ---------------------------------------------------------------------------
# 3. OLS for covariate-adjusted ITT (ANCOVA-style)
#    Model: Y = beta0 + beta1*T + beta2*baseline_score + beta3*baseline_income
#                 + beta4*age + beta5*female + e
#    beta1 is the adjusted ITT effect under linearity/additivity assumptions.
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
    """
    OLS via normal equations with homoskedastic SEs.
    Returns coefficients and standard errors.
    """
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
# 4. Analysis functions
# ---------------------------------------------------------------------------
def split_arms(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    treated = [r for r in rows if r["treat"] == 1]
    control = [r for r in rows if r["treat"] == 0]
    return treated, control


def complete_cases(rows: list[dict], outcome: str) -> list[dict]:
    return [r for r in rows if r[outcome] is not None]


def print_consort(rows: list[dict], outcome: str) -> None:
    treated, control = split_arms(rows)
    analyzed = complete_cases(rows, outcome)
    analyzed_t = [r for r in analyzed if r["treat"] == 1]
    analyzed_c = [r for r in analyzed if r["treat"] == 0]

    print("=" * 72)
    print("CONSORT-style flow (mock)")
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
    print("Notes: Balance tests are diagnostic; randomization is the identifying device.")
    print()


def print_primary_itt(rows: list[dict], outcome: str) -> TwoSampleResult:
    analyzed = complete_cases(rows, outcome)
    t_vals = [r[outcome] for r in analyzed if r["treat"] == 1]
    c_vals = [r[outcome] for r in analyzed if r["treat"] == 0]
    res = welch_two_sample(t_vals, c_vals)

    print("=" * 72)
    print("Primary analysis: ITT difference in means (unadjusted)")
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
    sig = "reject H0" if res.p_value < ALPHA else "fail to reject H0"
    print(f"Decision at alpha={ALPHA}: {sig}")
    print()
    return res


def print_adjusted_itt(rows: list[dict], outcome: str) -> None:
    analyzed = complete_cases(rows, outcome)
    y = [r[outcome] for r in analyzed]

    # Design matrix with intercept.
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
    print("Secondary / pre-specified adjusted ITT (ANCOVA-style OLS)")
    print("=" * 72)
    print("Model: post_income ~ treat + baseline_score + baseline_income + age + female")
    print(f"Adjusted ITT effect (treat): {b:,.2f}")
    print(f"SE:                        {se:,.2f}")
    print(f"95% CI:                    [{ci_low:,.2f}, {ci_high:,.2f}]")
    print(f"p-value (two-sided):       {p:,.4f}")
    print("Interpretation: association under linear adjustment; not a substitute")
    print("for design if randomization failed.")
    print()


def print_summary(primary: TwoSampleResult, true_ate: float) -> None:
    print("=" * 72)
    print("Summary (simulation benchmark)")
    print("=" * 72)
    print(f"Planted true ATE (simulation only): {true_ate:,.2f}")
    print(f"Estimated ITT (unadjusted):         {primary.diff:,.2f}")
    print(f"95% CI contains true ATE:           {primary.ci_low <= true_ate <= primary.ci_high}")
    print()
    print("Reporting checklist mirrored in this script:")
    print("  [x] Estimand stated (ITT-ATE)")
    print("  [x] Randomization + arm sizes")
    print("  [x] Attrition / analyzed N")
    print("  [x] Balance table with SMD")
    print("  [x] Primary unadjusted ITT with CI and p-value")
    print("  [x] Covariate-adjusted ITT (secondary/specified)")
    print("  [ ] Multiplicity adjustment (not needed for one primary endpoint)")
    print("  [ ] Pre-registration link / protocol (omitted in mock)")


# ---------------------------------------------------------------------------
# 5. Run full analysis pipeline on mock data
# ---------------------------------------------------------------------------
def main() -> None:
    print("=" * 72)
    print(TRIAL_NAME)
    print("=" * 72)
    print(f"Primary estimand: ITT average treatment effect on {PRIMARY_OUTCOME}")
    print(f"Randomization: individual-level {RANDOMIZATION_RATIO[0]}:{RANDOMIZATION_RATIO[1]}")
    print(f"Significance level: alpha = {ALPHA}")
    print()

    data = generate_mock_trial(n=400, attrition_rate=0.08, true_ate=TRUE_ATE)

    print_consort(data, PRIMARY_OUTCOME)
    print_table1(data, BASELINE_COVARIATES)
    primary = print_primary_itt(data, PRIMARY_OUTCOME)
    print_adjusted_itt(data, PRIMARY_OUTCOME)
    print_summary(primary, TRUE_ATE)


if __name__ == "__main__":
    main()
