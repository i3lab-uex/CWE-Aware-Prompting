"""Matched mixed-model analysis and publication-ready figures for CWE runs."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator, PercentFormatter
import numpy as np
from numpy.polynomial.hermite import hermgauss
import pandas as pd
from scipy.optimize import minimize, minimize_scalar
from scipy.special import expit, gammaln, logsumexp
from scipy.stats import norm
import seaborn as sns

from cwe_experiment.storage import read_parquet


LEVEL_ORDER = ("Generic", "Pillar", "Class", "Base", "Variant", "Compound")
CWE_STRATIFIED_LEVELS = ("Pillar", "Class", "Base")
CWE_LOW_DENOMINATOR_THRESHOLD = 20
CWE_DENOMINATOR_FIELDS = {
    "capability_difference": ("generic_capability_n", "treatment_capability_n"),
    "safety_difference": ("generic_safety_n", "treatment_safety_n"),
    "target_cwe_reduction": ("generic_target_cwe_n", "treatment_target_cwe_n"),
}
COMMON_SUBSET_CONDITIONS = ("Generic", "Pillar", "Class", "Base")
COMMON_SUBSET_CONTRASTS = (
    ("Pillar", "Generic"),
    ("Class", "Generic"),
    ("Base", "Generic"),
    ("Class", "Base"),
)
TARGET_ABSTRACTION_ORDER = ("Base", "Class", "Variant", "Compound")
LEVEL_COLORS = {
    "Generic": "#52616b",
    "Pillar": "#315c89",
    "Class": "#327a67",
    "Base": "#c17a2b",
    "Variant": "#9b4f68",
    "Compound": "#73559b",
}
COMPLETE_ANALYZER_STATUS = "complete"
SECURITY_OUTCOME_NAMES = frozenset(
    {
        "safety_test_success",
        "target_cwe_present",
        "other_cwe_present",
        "finding_count",
    }
)


@dataclass(frozen=True)
class Outcome:
    name: str
    label: str
    family: str
    improvement_direction: int
    eligible: Callable[[dict[str, Any]], bool]
    value: Callable[[dict[str, Any]], float]


@dataclass
class MixedModelFit:
    family: str
    parameters: np.ndarray
    covariance: np.ndarray
    fixed_names: list[str]
    converged: bool
    message: str
    log_likelihood: float
    dispersion: float | None
    observations: int
    tasks: int

    @property
    def beta(self) -> np.ndarray:
        return self.parameters[: len(self.fixed_names)]

    @property
    def sigma(self) -> float:
        return float(np.exp(self.parameters[len(self.fixed_names)]))


def _nonpending_evaluation(row: dict[str, Any]) -> bool:
    return (
        row["generation_status"] == "ok"
        and row["evaluation_status"]
        not in {None, "pending", "skipped", "skipped_generation_error"}
    )


def _capability_test_success(row: dict[str, Any]) -> bool:
    """Strict request-level capability success; invalid responses are failures."""

    return (
        row.get("generation_status") == "ok"
        and int(row.get("capability_total") or 0) > 0
        and int(row.get("capability_passed") or 0)
        == int(row.get("capability_total") or 0)
    )


def _safety_test_success(row: dict[str, Any]) -> bool:
    return (
        int(row.get("safety_total") or 0) > 0
        and int(row.get("safety_passed") or 0)
        == int(row.get("safety_total") or 0)
    )


OUTCOMES = (
    Outcome(
        "overall_test_success",
        "All-test success (capability + safety)",
        "binomial",
        1,
        lambda row: True,
        lambda row: float(row.get("all_tests_pass") is True),
    ),
    Outcome(
        "capability_test_success",
        "Capability-test success (functional)",
        "binomial",
        1,
        lambda row: True,
        lambda row: float(_capability_test_success(row)),
    ),
    Outcome(
        "safety_test_success",
        "Safety-test success among capability-passing code",
        "binomial",
        1,
        lambda row: _capability_test_success(row)
        and int(row.get("safety_total") or 0) > 0,
        lambda row: float(_safety_test_success(row)),
    ),
    Outcome(
        "target_cwe_present",
        "Target-CWE finding among capability-passing code",
        "binomial",
        -1,
        lambda row: _capability_test_success(row)
        and bool(row["analyzer_observed"]),
        lambda row: float(int(row["target_finding_count"]) > 0),
    ),
    Outcome(
        "other_cwe_present",
        "Other-CWE finding among capability-passing code",
        "binomial",
        -1,
        lambda row: _capability_test_success(row)
        and bool(row["analyzer_observed"]),
        lambda row: float(int(row["other_finding_count"]) > 0),
    ),
    Outcome(
        "finding_count",
        "Analyzer findings among capability-passing code",
        "count",
        -1,
        lambda row: _capability_test_success(row)
        and bool(row["analyzer_observed"]),
        lambda row: float(row["finding_count"]),
    ),
)


def _write_csv(
    path: Path,
    rows: Iterable[dict[str, Any]],
    fieldnames: Sequence[str],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _checkpoint_rows(directory: Path) -> list[dict[str, Any]]:
    priority = {"generation": 0, "evaluation": 1, "analysis": 2}
    fragments = sorted(
        directory.glob("*.parquet"),
        key=lambda path: (priority.get(path.name.split("-", 1)[0], 3), path.name),
    )
    merged: dict[tuple[str, str, int], dict[str, Any]] = {}
    for fragment in fragments:
        for row in read_parquet(fragment):
            key = (
                str(row["task_id"]),
                str(row["cwe_level"]),
                int(row["generation_index"]),
            )
            merged[key] = row
    return list(merged.values())


def load_results(path: Path) -> list[dict[str, Any]]:
    """Read a compact result, run directory, or live checkpoint directory."""

    if path.is_file():
        return read_parquet(path)
    if not path.exists():
        raise FileNotFoundError(path)
    compact = path / "results.parquet"
    checkpoints = path / "checkpoints"
    if compact.exists():
        return read_parquet(compact)
    if checkpoints.is_dir():
        return _checkpoint_rows(checkpoints)
    if path.name == "checkpoints":
        return _checkpoint_rows(path)
    raise FileNotFoundError(f"No se encontraron results.parquet ni checkpoints en {path}")


def _finding_counts(row: dict[str, Any]) -> tuple[int, int, int]:
    findings = list(row.get("bandit_findings") or []) + list(
        row.get("codeql_findings") or []
    )
    target = int(row["target_cwe"])
    target_count = sum(finding.get("cwe") == target for finding in findings)
    other_count = sum(
        finding.get("cwe") is not None and finding.get("cwe") != target
        for finding in findings
    )
    return len(findings), target_count, other_count


def flatten_rows(
    rows: Iterable[dict[str, Any]],
    *,
    analyzer_policy: str,
) -> list[dict[str, Any]]:
    flattened: list[dict[str, Any]] = []
    for row in rows:
        bandit_complete = row.get("bandit_status") == COMPLETE_ANALYZER_STATUS
        codeql_complete = row.get("codeql_status") == COMPLETE_ANALYZER_STATUS
        analyzer_observed = (
            bandit_complete and codeql_complete
            if analyzer_policy == "all"
            else bandit_complete or codeql_complete
        )
        finding_count, target_count, other_count = _finding_counts(row)
        flattened.append(
            {
                **row,
                "model": str(row.get("model") or "unknown"),
                "task_id": str(row["task_id"]),
                "cwe_level": str(row["cwe_level"]),
                "analyzer_observed": analyzer_observed,
                "finding_count": finding_count,
                "target_finding_count": target_count,
                "other_finding_count": other_count,
            }
        )
    return flattened


def matched_rows(
    rows: Sequence[dict[str, Any]],
    outcome: Outcome,
    treatment: str,
    *,
    generic: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    model_stats: list[dict[str, Any]] = []
    for model in sorted({str(row["model"]) for row in rows}):
        model_rows = [row for row in rows if row["model"] == model]
        generic_tasks = {
            row["task_id"] for row in model_rows if row["cwe_level"] == generic
        }
        treatment_tasks = {
            row["task_id"] for row in model_rows if row["cwe_level"] == treatment
        }
        matched_tasks = generic_tasks & treatment_tasks
        eligible = [
            row
            for row in model_rows
            if row["task_id"] in matched_tasks
            and row["cwe_level"] in {generic, treatment}
            and outcome.eligible(row)
        ]
        selected.extend(eligible)
        model_stats.append(
            {
                "model": model,
                "generic_supported_tasks": len(generic_tasks),
                "treatment_supported_tasks": len(treatment_tasks),
                "matched_tasks": len(matched_tasks),
                "generic_observations": sum(
                    row["cwe_level"] == generic for row in eligible
                ),
                "treatment_observations": sum(
                    row["cwe_level"] == treatment for row in eligible
                ),
            }
        )
    summary = {
        "outcome": outcome.name,
        "contrast": f"{treatment} vs {generic}",
        "treatment": treatment,
        "models": model_stats,
    }
    return selected, summary


def common_condition_subset(
    rows: Sequence[dict[str, Any]],
    *,
    conditions: Sequence[str] = COMMON_SUBSET_CONDITIONS,
) -> list[dict[str, Any]]:
    """Keep model-task pairs that structurally support every named condition."""

    required = set(conditions)
    if len(required) != len(conditions):
        raise ValueError("conditions must be distinct")
    supported: dict[tuple[str, str], set[str]] = {}
    for row in rows:
        key = (str(row["model"]), str(row["task_id"]))
        supported.setdefault(key, set()).add(str(row["cwe_level"]))
    complete = {
        key for key, levels in supported.items() if required.issubset(levels)
    }
    return [
        row
        for row in rows
        if (str(row["model"]), str(row["task_id"])) in complete
        and str(row["cwe_level"]) in required
    ]


def target_abstraction_distribution(
    rows: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Count retained tasks by the abstraction of their target CWE node."""

    task_levels: dict[str, str] = {}
    task_targets: dict[str, int] = {}
    for row in rows:
        prompt_cwe = row.get("prompt_cwe")
        target_cwe = row.get("target_cwe")
        if prompt_cwe is None or target_cwe is None:
            continue
        try:
            is_target = int(prompt_cwe) == int(target_cwe)
        except (TypeError, ValueError):
            is_target = str(prompt_cwe) == str(target_cwe)
        if not is_target:
            continue
        task_id = str(row["task_id"])
        level = str(row["cwe_level"])
        target = int(target_cwe)
        previous_level = task_levels.setdefault(task_id, level)
        previous_target = task_targets.setdefault(task_id, target)
        if previous_level != level or previous_target != target:
            raise ValueError(
                f"Inconsistent target abstraction metadata for task {task_id}"
            )

    counts: dict[str, int] = {}
    for level in task_levels.values():
        counts[level] = counts.get(level, 0) + 1
    ordered_levels = [
        level for level in TARGET_ABSTRACTION_ORDER if level in counts
    ]
    ordered_levels.extend(sorted(set(counts) - set(TARGET_ABSTRACTION_ORDER)))
    total = len(task_levels)
    return [
        {
            "target_abstraction": level,
            "tasks": counts[level],
            "percentage": counts[level] / total if total else 0.0,
        }
        for level in ordered_levels
    ]


def _design_matrix(
    rows: Sequence[dict[str, Any]],
    treatment: str,
    generic: str,
) -> tuple[np.ndarray, list[str], list[str]]:
    models = sorted({str(row["model"]) for row in rows})
    reference = models[0]
    names = ["Intercept", f"{treatment}_vs_{generic}"]
    names.extend(f"model[{model}]" for model in models[1:])
    names.extend(f"{treatment}:model[{model}]" for model in models[1:])
    matrix: list[list[float]] = []
    for row in rows:
        is_treatment = float(row["cwe_level"] == treatment)
        model = str(row["model"])
        vector = [1.0, is_treatment]
        vector.extend(float(model == item) for item in models[1:])
        vector.extend(is_treatment * float(model == item) for item in models[1:])
        matrix.append(vector)
    assert reference == models[0]
    return np.asarray(matrix, dtype=float), names, models


def _prediction_vector(
    model: str,
    *,
    treatment: bool,
    models: Sequence[str],
) -> np.ndarray:
    value = float(treatment)
    vector = [1.0, value]
    vector.extend(float(model == item) for item in models[1:])
    vector.extend(value * float(model == item) for item in models[1:])
    return np.asarray(vector, dtype=float)


def _clusters(
    rows: Sequence[dict[str, Any]],
    x: np.ndarray,
    y: np.ndarray,
) -> list[tuple[np.ndarray, np.ndarray]]:
    grouped: dict[str, list[int]] = {}
    for index, row in enumerate(rows):
        grouped.setdefault(str(row["task_id"]), []).append(index)
    return [(x[indexes], y[indexes]) for indexes in grouped.values()]


def _log_probability(y: np.ndarray, eta: np.ndarray, family: str, alpha: float) -> np.ndarray:
    if family == "binomial":
        return y * -np.logaddexp(0.0, -eta) + (1.0 - y) * -np.logaddexp(0.0, eta)
    eta = np.clip(eta, -30.0, 30.0)
    mu = np.exp(eta)
    if family == "poisson":
        return y * eta - mu - gammaln(y + 1.0)
    size = 1.0 / alpha
    return (
        gammaln(y + size)
        - gammaln(size)
        - gammaln(y + 1.0)
        + size * (np.log(size) - np.log(size + mu))
        + y * (np.log(mu) - np.log(size + mu))
    )


def _initial_beta(x: np.ndarray, y: np.ndarray, family: str) -> np.ndarray:
    if family == "binomial":
        transformed = math.log((float(y.mean()) + 0.01) / (1.01 - float(y.mean())))
    else:
        transformed = math.log(max(float(y.mean()), 0.05))
    beta = np.zeros(x.shape[1], dtype=float)
    beta[0] = transformed
    return beta


def _numerical_hessian(function: Callable[[np.ndarray], float], point: np.ndarray) -> np.ndarray:
    size = len(point)
    steps = 2e-4 * np.maximum(1.0, np.abs(point))
    result = np.empty((size, size), dtype=float)
    center = function(point)
    for i in range(size):
        plus = point.copy()
        minus = point.copy()
        plus[i] += steps[i]
        minus[i] -= steps[i]
        result[i, i] = (function(plus) - 2.0 * center + function(minus)) / steps[i] ** 2
        for j in range(i):
            pp = point.copy()
            pm = point.copy()
            mp = point.copy()
            mm = point.copy()
            pp[i] += steps[i]
            pp[j] += steps[j]
            pm[i] += steps[i]
            pm[j] -= steps[j]
            mp[i] -= steps[i]
            mp[j] += steps[j]
            mm[i] -= steps[i]
            mm[j] -= steps[j]
            value = (
                function(pp) - function(pm) - function(mp) + function(mm)
            ) / (4.0 * steps[i] * steps[j])
            result[i, j] = value
            result[j, i] = value
    return result


def _safe_covariance(hessian: np.ndarray) -> np.ndarray:
    symmetric = (hessian + hessian.T) / 2.0
    values, vectors = np.linalg.eigh(symmetric)
    floor = max(float(np.max(np.abs(values))) * 1e-8, 1e-8)
    inverse = vectors @ np.diag(1.0 / np.maximum(values, floor)) @ vectors.T
    return (inverse + inverse.T) / 2.0


def fit_mixed_glm(
    rows: Sequence[dict[str, Any]],
    outcome: Outcome,
    treatment: str,
    *,
    generic: str,
    family: str,
    quadrature_points: int,
) -> tuple[MixedModelFit, list[str]]:
    warnings: list[str] = []
    x, fixed_names, _ = _design_matrix(rows, treatment, generic)
    y = np.asarray([outcome.value(row) for row in rows], dtype=float)
    clustered = _clusters(rows, x, y)
    nodes, weights = hermgauss(quadrature_points)
    log_weights = np.log(weights) - 0.5 * math.log(math.pi)
    fixed_count = x.shape[1]
    parameter_count = fixed_count + 1 + int(family == "negative_binomial")

    def objective(parameters: np.ndarray) -> float:
        beta = parameters[:fixed_count]
        sigma = math.exp(float(parameters[fixed_count]))
        alpha = (
            math.exp(float(parameters[fixed_count + 1]))
            if family == "negative_binomial"
            else 1.0
        )
        total = 0.0
        offsets = math.sqrt(2.0) * sigma * nodes
        for cluster_x, cluster_y in clustered:
            base = cluster_x @ beta
            conditional = np.asarray(
                [
                    _log_probability(cluster_y, base + offset, family, alpha).sum()
                    for offset in offsets
                ]
            )
            total += float(logsumexp(log_weights + conditional))
        return -total if math.isfinite(total) else 1e100

    initial_beta = _initial_beta(x, y, family)
    starts: list[np.ndarray] = []
    for sigma in (0.15, 0.6, 1.5):
        initial = np.concatenate([initial_beta, [math.log(sigma)]])
        if family == "negative_binomial":
            initial = np.concatenate([initial, [math.log(0.5)]])
        starts.append(initial)
    bounds = [(-15.0, 15.0)] * fixed_count + [(-7.0, 3.0)]
    if family == "negative_binomial":
        bounds.append((-7.0, 5.0))
    attempts = [
        minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 2000, "ftol": 1e-10, "gtol": 1e-6},
        )
        for start in starts
    ]
    result = min(attempts, key=lambda item: float(item.fun))
    if not result.success:
        warnings.append(f"optimización: {result.message}")
    boundary_indexes: set[int] = set()
    if result.x[fixed_count] <= -6.99:
        warnings.append("varianza del intercepto aleatorio en el límite inferior")
        boundary_indexes.add(fixed_count)
    elif result.x[fixed_count] >= 2.99:
        warnings.append("varianza del intercepto aleatorio en el límite superior")
        boundary_indexes.add(fixed_count)
    if family == "negative_binomial" and result.x[fixed_count + 1] <= -6.99:
        warnings.append("sobredispersión negativo-binomial en el límite inferior")
        boundary_indexes.add(fixed_count + 1)
    hessian = _numerical_hessian(objective, np.asarray(result.x, dtype=float))
    if boundary_indexes:
        free = [
            index for index in range(parameter_count) if index not in boundary_indexes
        ]
        covariance = np.zeros_like(hessian)
        covariance[np.ix_(free, free)] = _safe_covariance(
            hessian[np.ix_(free, free)]
        )
    else:
        covariance = _safe_covariance(hessian)
    fit = MixedModelFit(
        family=family,
        parameters=np.asarray(result.x, dtype=float),
        covariance=covariance,
        fixed_names=fixed_names,
        converged=bool(result.success),
        message=str(result.message),
        log_likelihood=-float(result.fun),
        dispersion=None,
        observations=len(rows),
        tasks=len(clustered),
    )
    if parameter_count != len(fit.parameters):
        raise AssertionError("unexpected model parameter count")
    return fit, warnings


def _conditional_mean(
    parameters: np.ndarray,
    vector: np.ndarray,
    family: str,
    fixed_count: int,
) -> float:
    linear = float(vector @ parameters[:fixed_count])
    if family == "binomial":
        return float(expit(linear))
    return float(math.exp(min(linear, 30.0)))


def _poisson_dispersion(
    fit: MixedModelFit,
    rows: Sequence[dict[str, Any]],
    outcome: Outcome,
    treatment: str,
    generic: str,
) -> float:
    x, _, _ = _design_matrix(rows, treatment, generic)
    y = np.asarray([outcome.value(row) for row in rows], dtype=float)
    indexes_by_task: dict[str, list[int]] = {}
    for index, row in enumerate(rows):
        indexes_by_task.setdefault(str(row["task_id"]), []).append(index)
    squared = 0.0
    sigma = fit.sigma
    for indexes in indexes_by_task.values():
        cluster_x = x[indexes]
        cluster_y = y[indexes]
        base = cluster_x @ fit.beta

        def posterior_objective(random_intercept: float) -> float:
            eta = np.clip(base + random_intercept, -30.0, 30.0)
            penalty = (
                random_intercept**2 / (2.0 * sigma**2)
                if sigma > 1e-6
                else 0.0
            )
            return float(np.exp(eta).sum() - cluster_y @ eta + penalty)

        random_intercept = (
            float(
                minimize_scalar(
                    posterior_objective,
                    bounds=(-12.0, 12.0),
                    method="bounded",
                ).x
            )
            if sigma > 1e-6
            else 0.0
        )
        means = np.exp(np.clip(base + random_intercept, -30.0, 30.0))
        squared += float(np.sum((cluster_y - means) ** 2 / np.maximum(means, 1e-9)))
    return squared / max(len(rows) - len(fit.fixed_names), 1)


def _draw_parameters(
    fit: MixedModelFit,
    draws: int,
    seed: int,
) -> np.ndarray:
    random = np.random.default_rng(seed)
    values = random.multivariate_normal(
        fit.parameters,
        fit.covariance,
        size=draws,
        check_valid="ignore",
    )
    fixed_count = len(fit.fixed_names)
    values[:, fixed_count] = np.clip(values[:, fixed_count], -7.0, 3.0)
    if fit.family == "negative_binomial":
        values[:, fixed_count + 1] = np.clip(
            values[:, fixed_count + 1], -7.0, 5.0
        )
    return values


def _quantile_interval(values: Sequence[float]) -> tuple[float, float]:
    low, high = np.quantile(np.asarray(values, dtype=float), [0.025, 0.975])
    return float(low), float(high)


def summarize_fit(
    fit: MixedModelFit,
    rows: Sequence[dict[str, Any]],
    outcome: Outcome,
    treatment: str,
    *,
    generic: str,
    ci_draws: int,
    seed: int,
) -> list[dict[str, Any]]:
    _, _, models = _design_matrix(rows, treatment, generic)
    parameters = _draw_parameters(fit, ci_draws, seed)
    fixed_count = len(fit.fixed_names)
    result: list[dict[str, Any]] = []
    for model in models:
        generic_vector = _prediction_vector(
            model, treatment=False, models=models
        )
        treatment_vector = _prediction_vector(
            model, treatment=True, models=models
        )
        contrast = treatment_vector - generic_vector
        coefficient = float(contrast @ fit.beta)
        coefficient_variance = float(
            contrast @ fit.covariance[:fixed_count, :fixed_count] @ contrast
        )
        coefficient_se = math.sqrt(max(coefficient_variance, 0.0))
        z_value = coefficient / coefficient_se if coefficient_se else math.inf
        p_value = float(2.0 * norm.sf(abs(z_value)))
        generic_estimate = _conditional_mean(
            fit.parameters, generic_vector, fit.family, fixed_count
        )
        treatment_estimate = _conditional_mean(
            fit.parameters, treatment_vector, fit.family, fixed_count
        )
        generic_draws = np.asarray(
            [
                _conditional_mean(value, generic_vector, fit.family, fixed_count)
                for value in parameters
            ]
        )
        treatment_draws = np.asarray(
            [
                _conditional_mean(value, treatment_vector, fit.family, fixed_count)
                for value in parameters
            ]
        )
        difference_draws = treatment_draws - generic_draws
        relative_draws = treatment_draws / np.maximum(generic_draws, 1e-12)
        generic_low, generic_high = _quantile_interval(generic_draws)
        treatment_low, treatment_high = _quantile_interval(treatment_draws)
        difference_low, difference_high = _quantile_interval(difference_draws)
        relative_low, relative_high = _quantile_interval(relative_draws)
        generic_n = sum(
            row["model"] == model and row["cwe_level"] == generic for row in rows
        )
        treatment_n = sum(
            row["model"] == model and row["cwe_level"] == treatment
            for row in rows
        )
        model_tasks = {
            row["task_id"] for row in rows if row["model"] == model
        }
        result.append(
            {

                "outcome": outcome.name,
                "outcome_label": outcome.label,
                "family": fit.family,
                "model": model,
                "contrast": f"{treatment} vs {generic}",
                "treatment": treatment,
                "generic": generic,
                "tasks": len(model_tasks),
                "generic_n": generic_n,
                "treatment_n": treatment_n,
                "generic_estimate": generic_estimate,
                "generic_ci_low": generic_low,
                "generic_ci_high": generic_high,
                "treatment_estimate": treatment_estimate,
                "treatment_ci_low": treatment_low,
                "treatment_ci_high": treatment_high,
                "absolute_difference": treatment_estimate - generic_estimate,
                "difference_ci_low": difference_low,
                "difference_ci_high": difference_high,
                "relative_measure": (
                    "risk_ratio" if outcome.family == "binomial" else "rate_ratio"
                ),
                "relative_effect": treatment_estimate / max(generic_estimate, 1e-12),
                "relative_ci_low": relative_low,
                "relative_ci_high": relative_high,
                "coefficient": coefficient,
                "coefficient_se": coefficient_se,
                "z_value": z_value,
                "p_value": p_value,
                "p_holm": None,
                "improvement": outcome.improvement_direction
                * (treatment_estimate - generic_estimate),
                "improvement_ci_low": min(
                    outcome.improvement_direction * difference_low,
                    outcome.improvement_direction * difference_high,
                ),
                "improvement_ci_high": max(
                    outcome.improvement_direction * difference_low,
                    outcome.improvement_direction * difference_high,
                ),
            }
        )
    return result


def summarize_interactions(
    fit: MixedModelFit,
    rows: Sequence[dict[str, Any]],
    outcome: Outcome,
    treatment: str,
    *,
    generic: str,
) -> list[dict[str, Any]]:
    _, _, models = _design_matrix(rows, treatment, generic)
    if len(models) < 2:
        return []
    fixed_count = len(fit.fixed_names)
    fixed_covariance = fit.covariance[:fixed_count, :fixed_count]
    reference_contrast = _prediction_vector(
        models[0], treatment=True, models=models
    ) - _prediction_vector(models[0], treatment=False, models=models)
    result: list[dict[str, Any]] = []
    for model in models[1:]:
        model_contrast = _prediction_vector(
            model, treatment=True, models=models
        ) - _prediction_vector(model, treatment=False, models=models)
        interaction = model_contrast - reference_contrast
        coefficient = float(interaction @ fit.beta)
        standard_error = math.sqrt(
            max(float(interaction @ fixed_covariance @ interaction), 0.0)
        )
        z_value = coefficient / standard_error if standard_error else math.inf
        result.append(
            {
                "outcome": outcome.name,
                "contrast": f"{treatment} vs {generic}",
                "model": model,
                "reference_model": models[0],
                "coefficient": coefficient,
                "coefficient_se": standard_error,
                "z_value": z_value,
                "p_value": float(2.0 * norm.sf(abs(z_value))),
                "p_holm": None,
            }
        )
    return result


def holm_adjust(
    p_values: Sequence[float],
    *,
    planned_comparisons: int | None = None,
) -> list[float]:
    if not p_values:
        return []
    order = sorted(range(len(p_values)), key=lambda index: p_values[index])
    adjusted = [1.0] * len(p_values)
    running = 0.0
    total = planned_comparisons or len(p_values)
    if total < len(p_values):
        raise ValueError("planned_comparisons no puede ser menor que el número de p-values")
    for rank, index in enumerate(order):
        candidate = min(1.0, (total - rank) * float(p_values[index]))
        running = max(running, candidate)
        adjusted[index] = running
    return adjusted


def apply_holm(
    rows: list[dict[str, Any]],
    *,
    planned_comparisons: int,
) -> None:
    """Adjust within outcomes and across the prespecified security family."""

    groups: dict[tuple[str, str], list[int]] = {}
    for index, row in enumerate(rows):
        groups.setdefault((str(row["outcome"]), str(row["model"])), []).append(index)
    for indexes in groups.values():
        adjusted = holm_adjust(
            [float(rows[index]["p_value"]) for index in indexes],
            planned_comparisons=planned_comparisons,
        )
        for index, value in zip(indexes, adjusted):
            rows[index]["p_holm_within_outcome"] = value

    family_groups: dict[tuple[str, str], list[int]] = {}
    for index, row in enumerate(rows):
        outcome = str(row["outcome"])
        multiplicity_family = (
            "security_conditional"
            if outcome in SECURITY_OUTCOME_NAMES
            else outcome
        )
        row["multiplicity_family"] = multiplicity_family
        family_groups.setdefault(
            (multiplicity_family, str(row["model"])), []
        ).append(index)
    for (family, _model), indexes in family_groups.items():
        planned_outcomes = (
            len(SECURITY_OUTCOME_NAMES)
            if family == "security_conditional"
            else 1
        )
        family_size = planned_comparisons * planned_outcomes
        adjusted = holm_adjust(
            [float(rows[index]["p_value"]) for index in indexes],
            planned_comparisons=family_size,
        )
        for index, value in zip(indexes, adjusted):
            rows[index]["multiplicity_planned_comparisons"] = family_size
            rows[index]["p_holm"] = value


def apply_interaction_holm(
    rows: list[dict[str, Any]],
    *,
    planned_comparisons: int,
) -> None:
    groups: dict[tuple[str, str], list[int]] = {}
    for index, row in enumerate(rows):
        groups.setdefault((str(row["outcome"]), str(row["model"])), []).append(index)
    for indexes in groups.values():
        adjusted = holm_adjust(
            [float(rows[index]["p_value"]) for index in indexes],
            planned_comparisons=planned_comparisons,
        )
        for index, value in zip(indexes, adjusted):
            rows[index]["p_holm"] = value


def descriptive_statistics(
    rows: Sequence[dict[str, Any]],
    treatments: Sequence[str],
    *,
    generic: str,
) -> list[dict[str, Any]]:
    levels = [generic, *treatments]
    result: list[dict[str, Any]] = []
    for outcome in OUTCOMES:
        for model in sorted({str(row["model"]) for row in rows}):
            for level in levels:
                values = [
                    outcome.value(row)
                    for row in rows
                    if row["model"] == model
                    and row["cwe_level"] == level
                    and outcome.eligible(row)
                ]
                if not values:
                    continue
                array = np.asarray(values, dtype=float)
                result.append(
                    {
                        "outcome": outcome.name,
                        "outcome_label": outcome.label,
                        "model": model,
                        "condition": level,
                        "tasks": len(
                            {
                                row["task_id"]
                                for row in rows
                                if row["model"] == model
                                and row["cwe_level"] == level
                                and outcome.eligible(row)
                            }
                        ),
                        "observations": len(array),
                        "events": int(array.sum()),
                        "mean": float(array.mean()),
                        "standard_deviation": float(array.std(ddof=1))
                        if len(array) > 1
                        else 0.0,
                        "q1": float(np.quantile(array, 0.25)),
                        "median": float(np.quantile(array, 0.5)),
                        "q3": float(np.quantile(array, 0.75)),
                        "minimum": float(array.min()),
                        "maximum": float(array.max()),
                    }
                )
    return result


def cwe_descriptive_statistics(
    rows: Sequence[dict[str, Any]],
    *,
    generic: str,
    treatment: str,
) -> list[dict[str, Any]]:
    """Compute matched, CWE-stratified observed rates for one contrast.

    These summaries are descriptive rather than confirmatory.  Tasks are first
    restricted to the intersection supporting both conditions within each
    model and target CWE.  Security rates then retain the same conditioning as
    the primary analysis: only capability-passing generations are eligible.
    """

    summaries: list[dict[str, Any]] = []
    groups = sorted(
        {
            (str(row["model"]), int(row["target_cwe"]))
            for row in rows
            if str(row["cwe_level"]) in {generic, treatment}
        },
        key=lambda item: (item[0], item[1]),
    )
    for model, target_cwe in groups:
        group = [
            row
            for row in rows
            if str(row["model"]) == model
            and int(row["target_cwe"]) == target_cwe
            and str(row["cwe_level"]) in {generic, treatment}
        ]
        task_sets = {
            condition: {
                str(row["task_id"])
                for row in group
                if str(row["cwe_level"]) == condition
            }
            for condition in (generic, treatment)
        }
        matched_tasks = task_sets[generic] & task_sets[treatment]
        if not matched_tasks:
            continue
        matched = [
            row for row in group if str(row["task_id"]) in matched_tasks
        ]
        summary: dict[str, Any] = {
            "model": model,
            "target_cwe": target_cwe,
            "generic": generic,
            "treatment": treatment,
            "matched_tasks": len(matched_tasks),
        }
        for condition, prefix in ((generic, "generic"), (treatment, "treatment")):
            selected = [
                row for row in matched if str(row["cwe_level"]) == condition
            ]
            capability_values = [
                float(_capability_test_success(row)) for row in selected
            ]
            safety_values = [
                float(_safety_test_success(row))
                for row in selected
                if _capability_test_success(row)
                and int(row.get("safety_total") or 0) > 0
            ]
            target_values = [
                float(int(row["target_finding_count"]) > 0)
                for row in selected
                if _capability_test_success(row)
                and bool(row["analyzer_observed"])
            ]
            for outcome_name, values in (
                ("capability", capability_values),
                ("safety", safety_values),
                ("target_cwe", target_values),
            ):
                summary[f"{prefix}_{outcome_name}_n"] = len(values)
                summary[f"{prefix}_{outcome_name}_events"] = int(sum(values))
                summary[f"{prefix}_{outcome_name}_rate"] = (
                    float(np.mean(values)) if values else math.nan
                )
        summary["capability_difference"] = (
            float(summary["treatment_capability_rate"])
            - float(summary["generic_capability_rate"])
        )
        summary["safety_difference"] = (
            float(summary["treatment_safety_rate"])
            - float(summary["generic_safety_rate"])
        )
        summary["target_cwe_reduction"] = (
            float(summary["generic_target_cwe_rate"])
            - float(summary["treatment_target_cwe_rate"])
        )
        summaries.append(summary)
    return summaries


def cwe_lineage_descriptive_statistics(
    rows: Sequence[dict[str, Any]],
    *,
    generic: str,
    treatments: Sequence[str],
) -> list[dict[str, Any]]:
    """Describe every available lineage condition within each target CWE.

    Each condition is matched separately to ``generic`` so that a CWE is only
    summarized over tasks that actually support that node of its canonical
    lineage. The result remains descriptive and does not add CWE-specific
    hypothesis tests.
    """

    summaries = [
        summary
        for treatment in dict.fromkeys(str(value) for value in treatments)
        if treatment != generic
        for summary in cwe_descriptive_statistics(
            rows,
            generic=generic,
            treatment=treatment,
        )
    ]
    level_rank = {
        level: index
        for index, level in enumerate(
            _level_order(str(summary["treatment"]) for summary in summaries)
        )
    }
    return sorted(
        summaries,
        key=lambda summary: (
            str(summary["model"]),
            int(summary["target_cwe"]),
            level_rank[str(summary["treatment"])],
        ),
    )


def coverage_statistics(rows: Sequence[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    coverage: list[dict[str, Any]] = []
    status_counts: list[dict[str, Any]] = []
    groups = sorted({(str(row["model"]), str(row["cwe_level"])) for row in rows})
    for model, level in groups:
        selected = [
            row for row in rows if row["model"] == model and row["cwe_level"] == level
        ]
        coverage.append(
            {
                "model": model,
                "condition": level,
                "rows": len(selected),
                "tasks": len({row["task_id"] for row in selected}),
                "generation_success": sum(
                    row["generation_status"] == "ok" for row in selected
                ),
                "generation_failures": sum(
                    row["generation_status"] != "ok" for row in selected
                ),
                "evaluation_observed": sum(
                    _nonpending_evaluation(row) for row in selected
                ),
                "evaluation_failures": sum(
                    row["evaluation_status"]
                    not in {None, "pending", "complete", "skipped_generation_error"}
                    for row in selected
                ),
                "capability_success": sum(
                    _capability_test_success(row) for row in selected
                ),
                "safety_observed": sum(
                    _capability_test_success(row)
                    and int(row.get("safety_total") or 0) > 0
                    for row in selected
                ),
                "analyzer_observed": sum(
                    bool(row["analyzer_observed"]) for row in selected
                ),
                "security_analyzer_cohort": sum(
                    _capability_test_success(row)
                    and bool(row["analyzer_observed"])
                    for row in selected
                ),
            }
        )
        for field in ("generation_status", "evaluation_status", "bandit_status", "codeql_status"):
            values = sorted({str(row.get(field)) for row in selected})
            for value in values:
                status_counts.append(
                    {
                        "model": model,
                        "condition": level,
                        "stage": field,
                        "status": value,
                        "count": sum(str(row.get(field)) == value for row in selected),
                    }
                )
    return coverage, status_counts


FIGURE_STEMS = (
    "binary-outcome-distributions",
    "test-outcome-flow",
    "finding-count-distribution",
    "adjusted-effects",
    "count-improvements",
    "pipeline-coverage",
    "cwe-stratified-effects",
)

PLOT_OUTCOME_LABELS = {
    "overall_test_success": "Joint capability + safety success",
    "capability_test_success": "Functional capability success",
    "safety_test_success": "Safety-test success | functional",
    "target_cwe_present": "Target-CWE presence | functional",
    "other_cwe_present": "Other-CWE presence | functional",
    "finding_count": "Total static-analysis findings | functional",
}

# The conditional safety-test model remains part of the analysis and its CSV
# exports, but is intentionally omitted from the compact adjusted-effects plot.
ADJUSTED_EFFECT_FIGURE_OUTCOMES = (
    "overall_test_success",
    "capability_test_success",
    "target_cwe_present",
    "other_cwe_present",
    "finding_count",
)


def _plot_theme() -> None:
    sns.set_theme(
        context="paper",
        style="ticks",
        font_scale=1.0,
        rc={
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#6d7772",
            "axes.linewidth": 0.7,
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.titleweight": "bold",
            "axes.titlesize": 9,
            "axes.labelsize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "grid.color": "#dfe5e2",
            "grid.linewidth": 0.55,
            "grid.alpha": 0.9,
            "legend.fontsize": 7,
            "legend.title_fontsize": 7,
            "figure.titlesize": 10,
            "font.family": "DejaVu Sans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        },
    )


def _save_figure(figure: plt.Figure, output: Path, stem: str) -> list[str]:
    filenames = []
    for extension, options in (
        ("png", {"dpi": 300}),
        ("pdf", {}),
    ):
        filename = f"{stem}.{extension}"
        figure.savefig(
            output / filename,
            bbox_inches="tight",
            pad_inches=0.04,
            facecolor="white",
            **options,
        )
        filenames.append(filename)
    plt.close(figure)
    return filenames


def _level_order(values: Iterable[str]) -> list[str]:
    present = set(values)
    ordered = [level for level in LEVEL_ORDER if level in present]
    return ordered + sorted(present - set(LEVEL_ORDER))


def _small_multiple_figure(
    panel_count: int,
    *,
    row_height: float,
    extra_height: float,
    center_last: bool = False,
) -> tuple[plt.Figure, list[plt.Axes]]:
    """Create a compact two-column publication layout."""

    ncols = 2 if panel_count > 1 else 1
    nrows = math.ceil(panel_count / ncols)
    figure = plt.figure(
        figsize=(7.2, max(3.1, row_height * nrows + extra_height))
    )
    grid_columns = 4 if panel_count == 5 and center_last else ncols
    grid = figure.add_gridspec(nrows, grid_columns)
    if panel_count == 5 and center_last:
        axes = [
            figure.add_subplot(grid[0, :2]),
            figure.add_subplot(grid[0, 2:]),
            figure.add_subplot(grid[1, :2]),
            figure.add_subplot(grid[1, 2:]),
            figure.add_subplot(grid[2, 1:3]),
        ]
    elif panel_count == 5:
        axes = [
            figure.add_subplot(grid[0, 0]),
            figure.add_subplot(grid[0, 1]),
            figure.add_subplot(grid[1, 0]),
            figure.add_subplot(grid[1, 1]),
            figure.add_subplot(grid[2, :]),
        ]
    else:
        axes = [
            figure.add_subplot(grid[index // ncols, index % ncols])
            for index in range(panel_count)
        ]
    return figure, axes


def plot_binary_distributions(
    descriptive: Sequence[dict[str, Any]],
    output: Path,
) -> list[str]:
    rows = [row for row in descriptive if row["outcome"] != "finding_count"]
    outcomes = [outcome for outcome in OUTCOMES if outcome.family == "binomial"]
    models = sorted({str(row["model"]) for row in rows})
    panels = [(outcome, model) for outcome in outcomes for model in models]
    figure, axes = _small_multiple_figure(
        len(panels),
        row_height=2.15,
        extra_height=0.65,
    )
    for panel_index, (axis, (outcome, model)) in enumerate(
        zip(axes, panels)
    ):
        panel = [
            row
            for row in rows
            if row["outcome"] == outcome.name and str(row["model"]) == model
        ]
        levels = _level_order(str(row["condition"]) for row in panel)
        panel.sort(key=lambda row: levels.index(str(row["condition"])))
        frame = pd.DataFrame(panel)
        sns.barplot(
            data=frame,
            x="mean",
            y="condition",
            order=levels,
            hue="condition",
            palette=LEVEL_COLORS,
            legend=False,
            ax=axis,
        )
        for patch, row in zip(axis.patches, panel):
            value = float(row["mean"])
            inside = value > 0.78
            axis.text(
                value - 0.015 if inside else value + 0.012,
                patch.get_y() + patch.get_height() / 2,
                f'{int(row["events"])}/{int(row["observations"])} · {value:.1%}',
                va="center",
                ha="right" if inside else "left",
                fontsize=6.5,
            )
        suffix = f" · {model}" if len(models) > 1 else ""
        panel_letter = chr(ord("A") + panel_index)
        axis.set_title(
            f"{panel_letter}  {PLOT_OUTCOME_LABELS[outcome.name]}{suffix}",
            loc="left",
            pad=4,
        )
        axis.set_ylabel("")
        maximum = max((float(row["mean"]) for row in panel), default=1.0)
        if outcome.name == "target_cwe_present":
            upper = max(0.03, math.ceil(maximum * 100) / 100 + 0.01)
        elif outcome.name == "other_cwe_present":
            upper = max(0.25, math.ceil(maximum * 10) / 10 + 0.05)
        else:
            upper = 1.0
        axis.set_xlim(0, upper)
        axis.xaxis.set_major_locator(MaxNLocator(nbins=5))
        axis.xaxis.set_major_formatter(PercentFormatter(1.0))
        axis.set_xlabel("Observed proportion")
        axis.grid(axis="x")
        axis.grid(axis="y", visible=False)
        sns.despine(ax=axis)
    figure.suptitle(
        "Observed outcome rates by prompt condition",
        x=0.06,
        y=0.995,
        ha="left",
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0, 1, 0.975), h_pad=1.0, w_pad=1.2)
    return _save_figure(figure, output, "binary-outcome-distributions")


def plot_count_distribution(
    rows: Sequence[dict[str, Any]],
    output: Path,
) -> list[str]:
    models = sorted({str(row["model"]) for row in rows})
    levels = _level_order(str(row["cwe_level"]) for row in rows)
    labels = [
        f"{model} · {level}" if len(models) > 1 else level
        for model in models
        for level in levels
    ]
    records = []
    for row in rows:
        if not (
            _capability_test_success(row)
            and row["analyzer_observed"]
        ):
            continue
        count = int(row["finding_count"])
        level = str(row["cwe_level"])
        model = str(row["model"])
        records.append(
            {
                "label": f"{model} · {level}" if len(models) > 1 else level,
                "count_bin": str(count) if count < 5 else "5+",
            }
        )
    bins = ["0", "1", "2", "3", "4", "5+"]
    frame = pd.DataFrame(records)
    table = (
        pd.crosstab(frame["label"], frame["count_bin"], normalize="index")
        .reindex(index=labels, columns=bins, fill_value=0.0)
    )
    palette = sns.color_palette("crest", n_colors=len(bins))
    figure, axis = plt.subplots(
        figsize=(7.2, max(3.2, 0.38 * len(labels) + 1.45))
    )
    left = np.zeros(len(table))
    for count_bin, color in zip(bins, palette):
        values = table[count_bin].to_numpy(dtype=float)
        bars = axis.barh(
            table.index,
            values,
            left=left,
            label=count_bin,
            color=color,
            edgecolor="white",
            linewidth=0.5,
        )
        for bar, value, start in zip(bars, values, left):
            if value >= 0.07:
                axis.text(
                    start + value / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.0%}",
                    ha="center",
                    va="center",
                    fontsize=6.5,
                    color="#18211d",
                )
        left += values
    sample_sizes = frame.groupby("label").size()
    for index, label in enumerate(table.index):
        axis.text(
            1.01,
            index,
            f"n={int(sample_sizes.get(label, 0))}",
            va="center",
            fontsize=6.5,
        )
    axis.set_xlim(0, 1.055)
    axis.invert_yaxis()
    axis.xaxis.set_major_formatter(PercentFormatter(1.0))
    axis.set_xlabel("Share of functional, analyzer-observed generations")
    axis.set_ylabel("")
    axis.set_title(
        "Analyzer finding-count distribution among functional code",
        loc="left",
        pad=5,
    )
    axis.legend(
        title="Findings",
        ncol=6,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.20),
        handlelength=1.8,
        columnspacing=1.25,
    )
    axis.grid(axis="x")
    axis.grid(axis="y", visible=False)
    sns.despine(ax=axis)
    figure.tight_layout(rect=(0, 0.08, 1, 1))
    return _save_figure(figure, output, "finding-count-distribution")


def plot_test_outcome_flow(
    rows: Sequence[dict[str, Any]],
    output: Path,
) -> list[str]:
    """Show the sequential capability/safety outcome for every planned row."""

    models = sorted({str(row["model"]) for row in rows})
    levels = _level_order(str(row["cwe_level"]) for row in rows)
    labels = [
        f"{model} · {level}" if len(models) > 1 else level
        for model in models
        for level in levels
    ]
    records: list[dict[str, Any]] = []
    for model in models:
        for level in levels:
            selected = [
                row
                for row in rows
                if row["model"] == model and row["cwe_level"] == level
            ]
            total = len(selected)
            capability = sum(_capability_test_success(row) for row in selected)
            joint = sum(row.get("all_tests_pass") is True for row in selected)
            records.append(
                {
                    "label": (
                        f"{model} · {level}" if len(models) > 1 else level
                    ),
                    "total": total,
                    "Capability failure": total - capability,
                    "Capability pass; safety failure": max(capability - joint, 0),
                    "Capability + safety pass": joint,
                }
            )
    categories = (
        "Capability failure",
        "Capability pass; safety failure",
        "Capability + safety pass",
    )
    colors = ("#aeb8b3", "#c17a2b", "#327a67")
    figure, axis = plt.subplots(
        figsize=(7.2, max(3.2, 0.40 * len(records) + 1.35))
    )
    left = np.zeros(len(records), dtype=float)
    for category, color in zip(categories, colors):
        values = np.asarray(
            [
                record[category] / max(int(record["total"]), 1)
                for record in records
            ],
            dtype=float,
        )
        bars = axis.barh(
            labels,
            values,
            left=left,
            label=category,
            color=color,
            edgecolor="white",
            linewidth=0.6,
        )
        for bar, value, start in zip(bars, values, left):
            if value >= 0.055:
                axis.text(
                    start + value / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.1%}",
                    ha="center",
                    va="center",
                    fontsize=6.5,
                    color="#17201c",
                )
        left += values
    for index, record in enumerate(records):
        axis.text(
            1.01,
            index,
            f'n={int(record["total"])}',
            va="center",
            fontsize=6.5,
        )
    axis.set_xlim(0, 1.055)
    axis.invert_yaxis()
    axis.xaxis.set_major_formatter(PercentFormatter(1.0))
    axis.set_xlabel("Share of all planned generations")
    axis.set_ylabel("")
    axis.set_title(
        "Sequential outcomes: functional capability first, then safety",
        loc="left",
        pad=5,
    )
    axis.legend(
        frameon=False,
        ncol=3,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        columnspacing=1.2,
    )
    axis.grid(axis="x")
    axis.grid(axis="y", visible=False)
    sns.despine(ax=axis)
    figure.tight_layout(rect=(0, 0.07, 1, 1))
    return _save_figure(figure, output, "test-outcome-flow")


def plot_improvements(
    model_rows: Sequence[dict[str, Any]],
    output: Path,
    *,
    family: str,
) -> list[str]:
    if family == "all":
        rows = list(model_rows)
    elif family == "count":
        rows = [
            row for row in model_rows
            if str(row["outcome"]) == "finding_count"
        ]
    else:
        raise ValueError(f"Familia de figura no soportada: {family}")
    models = {str(row["model"]) for row in rows}
    records: list[dict[str, Any]] = []
    for row in rows:
        if family == "all":
            relative = max(float(row["relative_effect"]), 1e-12)
            relative_low = max(float(row["relative_ci_low"]), 1e-12)
            relative_high = max(float(row["relative_ci_high"]), 1e-12)
            estimate, low, high = relative, relative_low, relative_high
            unstable = estimate > 100.0 or relative_high > 10_000.0
            measure = (
                "IRR" if str(row["outcome"]) == "finding_count" else "RR"
            )
        else:
            estimate = float(row["improvement"])
            low = float(row["improvement_ci_low"])
            high = float(row["improvement_ci_high"])
            unstable = False
            measure = "absolute"
        unstable = unstable or not all(
            math.isfinite(value) for value in (estimate, low, high)
        )
        records.append(
            {
                "outcome": str(row["outcome"]),
                "model": str(row["model"]),
                "estimate": estimate,
                "low": low,
                "high": high,
                "measure": measure,
                "unstable": unstable,
                "treatment": str(row["treatment"]),
                "significant": float(row["p_holm"]) < 0.05,
                "p_holm": float(row["p_holm"]),
            }
        )
    treatment_key = lambda record: (
        str(record["model"]),
        LEVEL_ORDER.index(str(record["treatment"]))
        if str(record["treatment"]) in LEVEL_ORDER
        else 99,
    )

    if family == "all":
        outcome_names = [
            outcome.name
            for outcome in OUTCOMES
            if outcome.name in ADJUSTED_EFFECT_FIGURE_OUTCOMES
            and any(record["outcome"] == outcome.name for record in records)
        ]
        figure, axes = _small_multiple_figure(
            len(outcome_names),
            row_height=2.15,
            extra_height=0.80,
            center_last=True,
        )
        display_low, display_high = 0.05, 10.0
        for panel_index, (axis, outcome_name) in enumerate(
            zip(axes, outcome_names)
        ):
            outcome_records = [
                record
                for record in records
                if record["outcome"] == outcome_name
            ]
            record_lookup = {
                (str(record["model"]), str(record["treatment"])): record
                for record in outcome_records
            }
            panel = []
            for model in sorted(models):
                for treatment in LEVEL_ORDER[1:]:
                    panel.append(
                        record_lookup.get(
                            (model, treatment),
                            {
                                "outcome": outcome_name,
                                "model": model,
                                "estimate": math.nan,
                                "low": math.nan,
                                "high": math.nan,
                                "measure": (
                                    "IRR"
                                    if outcome_name == "finding_count"
                                    else "RR"
                                ),
                                "unstable": True,
                                "treatment": treatment,
                                "significant": False,
                                "p_holm": math.nan,
                            },
                        )
                    )
            for y, record in enumerate(panel):
                color = LEVEL_COLORS.get(record["treatment"], "#315c89")
                if record["unstable"]:
                    axis.text(
                        0.03,
                        y,
                        "NE",
                        transform=axis.get_yaxis_transform(),
                        ha="left",
                        va="center",
                        fontsize=6.5,
                        fontstyle="italic",
                        color="#6d7772",
                    )
                    continue
                axis.hlines(
                    y,
                    max(float(record["low"]), display_low),
                    min(float(record["high"]), display_high),
                    color=color,
                    linewidth=1.5,
                    zorder=2,
                )
                if float(record["low"]) < display_low:
                    axis.scatter(
                        display_low,
                        y,
                        marker="<",
                        color=color,
                        s=16,
                        zorder=3,
                    )
                if float(record["high"]) > display_high:
                    axis.scatter(
                        display_high,
                        y,
                        marker=">",
                        color=color,
                        s=16,
                        zorder=3,
                    )
                displayed = min(
                    max(float(record["estimate"]), display_low),
                    display_high,
                )
                axis.scatter(
                    displayed,
                    y,
                    marker="D" if record["significant"] else "o",
                    color=color,
                    edgecolor="white",
                    linewidth=0.5,
                    s=31 if record["significant"] else 27,
                    zorder=4,
                )
                # Keep estimates in a dedicated column outside the plotting
                # area.  Labels attached to the points collide vertically
                # when the figure is reduced to manuscript column width.
                axis.text(
                    1.015,
                    y,
                    f'{float(record["estimate"]):.2f}',
                    transform=axis.get_yaxis_transform(),
                    ha="left",
                    va="center",
                    fontsize=6,
                    clip_on=False,
                )
            axis.set_xscale("log")
            axis.set_xlim(display_low, display_high)
            axis.set_xticks(
                [0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0]
            )
            axis.set_xticklabels(
                ["0.05", "0.1", "0.25", "0.5", "1", "2", "4", "10"]
            )
            axis.axvline(1.0, color="#4c5751", linewidth=0.9, zorder=1)
            axis.set_yticks(range(len(panel)))
            axis.set_yticklabels(
                [
                    (
                        f'{record["model"]} · {record["treatment"]}'
                        if len(models) > 1
                        else str(record["treatment"])
                    )
                    for record in panel
                ]
            )
            axis.invert_yaxis()
            axis.set_ylim(len(panel) - 0.55, -0.65)
            measure = "IRR" if outcome_name == "finding_count" else "Risk ratio"
            axis.set_xlabel(f"{measure} (log scale)")
            axis.set_ylabel("")
            axis.set_title(
                f"{chr(ord('A') + panel_index)}  "
                f"{PLOT_OUTCOME_LABELS[outcome_name]}",
                loc="left",
                pad=4,
            )
            axis.grid(axis="x")
            axis.grid(axis="y", visible=False)
            sns.despine(ax=axis)
        figure.suptitle(
            "Adjusted effects of CWE-informed prompting relative to Generic",
            x=0.06,
            y=0.995,
            ha="left",
            fontweight="bold",
        )
        figure.legend(
            handles=[
                Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="#52616b",
                    linestyle="none",
                    markeredgecolor="white",
                    label="Not significant",
                ),
                Line2D(
                    [0],
                    [0],
                    marker="D",
                    color="#327a67",
                    linestyle="none",
                    markeredgecolor="white",
                    label="Holm-adjusted p < 0.05",
                ),
            ],
            frameon=False,
            ncol=2,
            loc="lower center",
            bbox_to_anchor=(0.5, 0.005),
        )
        stem = "adjusted-effects"
        panel_letters = {
            outcome_name: chr(ord("A") + index)
            for index, outcome_name in enumerate(outcome_names)
        }
        higher_is_better = [
            panel_letters[outcome_name]
            for outcome_name in outcome_names
            if outcome_name
            in {"overall_test_success", "capability_test_success"}
        ]
        lower_is_better = [
            panel_letters[outcome_name]
            for outcome_name in outcome_names
            if outcome_name
            in {"target_cwe_present", "other_cwe_present", "finding_count"}
        ]

        def panel_span(letters: Sequence[str]) -> str:
            return letters[0] if len(letters) == 1 else f"{letters[0]}-{letters[-1]}"

        direction_notes = []
        if higher_is_better:
            direction_notes.append(
                f"{panel_span(higher_is_better)}: RR >1 favors the "
                "CWE-informed condition."
            )
        if lower_is_better:
            direction_notes.append(
                f"{panel_span(lower_is_better)}: RR/IRR <1 favors it."
            )
        figure.text(
            0.06,
            0.06,
            " ".join(direction_notes)
            + " Bars are pointwise 95% CIs.\n"
            "NE = not estimable because of separation/quasi-separation; no "
            "estimate or interval is plotted.",
            ha="left",
            va="bottom",
            fontsize=6.5,
        )
        figure.tight_layout(rect=(0, 0.13, 1, 0.97), h_pad=1.35, w_pad=2.2)
    else:
        ordered = sorted(records, key=treatment_key)
        figure, axis = plt.subplots(
            figsize=(7.2, max(2.7, 0.42 * max(len(ordered), 1) + 1.2))
        )
        for y, record in enumerate(ordered):
            color = LEVEL_COLORS.get(record["treatment"], "#315c89")
            axis.hlines(
                y,
                float(record["low"]),
                float(record["high"]),
                color=color,
                linewidth=1.6,
                zorder=2,
            )
            axis.scatter(
                float(record["estimate"]),
                y,
                marker="D" if record["significant"] else "o",
                color=color,
                edgecolor="white",
                linewidth=0.5,
                s=34 if record["significant"] else 29,
                zorder=3,
            )
            axis.annotate(
                f'{float(record["estimate"]):+.3f}'
                + ("*" if record["significant"] else ""),
                (float(record["estimate"]), y),
                xytext=(4, 4),
                textcoords="offset points",
                ha="left",
                va="bottom",
                fontsize=6.5,
            )
        bound = max(
            (
                abs(float(record[key]))
                for record in ordered
                for key in ("low", "high")
            ),
            default=0.25,
        )
        bound = max(bound, 0.05) * 1.12
        axis.set_xlim(-bound, bound)
        axis.axvline(0, color="#4c5751", linewidth=0.9, zorder=1)
        axis.set_yticks(range(len(ordered)))
        axis.set_yticklabels(
            [
                (
                    f'{record["model"]} · {record["treatment"]}'
                    if len(models) > 1
                    else str(record["treatment"])
                )
                for record in ordered
            ]
        )
        axis.invert_yaxis()
        axis.set_ylim(len(ordered) - 0.55, -0.65)
        axis.set_xlabel("Estimated reduction in findings per functional generation")
        axis.set_ylabel("")
        axis.set_title(
            "Adjusted change in analyzer finding counts relative to Generic\n"
            "Pointwise 95% CIs; positive values favor the CWE-informed condition",
            loc="left",
            pad=5,
        )
        axis.grid(axis="x")
        axis.grid(axis="y", visible=False)
        sns.despine(ax=axis)
        stem = "count-improvements"
        figure.tight_layout()
    return _save_figure(figure, output, stem)


def plot_coverage(
    coverage: Sequence[dict[str, Any]],
    output: Path,
) -> list[str]:
    models = {str(row["model"]) for row in coverage}
    ordered_coverage = sorted(
        coverage,
        key=lambda row: (
            str(row["model"]),
            LEVEL_ORDER.index(str(row["condition"]))
            if str(row["condition"]) in LEVEL_ORDER
            else 99,
        ),
    )
    records = []
    for row in ordered_coverage:
        total = max(int(row["rows"]), 1)
        label = (
            f'{row["model"]} · {row["condition"]}'
            if len(models) > 1
            else str(row["condition"])
        )
        for stage, field in (
            ("Generation", "generation_success"),
            ("Capability success", "capability_success"),
            ("Security analyzer cohort", "security_analyzer_cohort"),
        ):
            records.append(
                {
                    "label": label,
                    "stage": stage,
                    "coverage": int(row[field]) / total,
                }
            )
    frame = pd.DataFrame(records)
    order = [
        (
            f'{row["model"]} · {row["condition"]}'
            if len(models) > 1
            else str(row["condition"])
        )
        for row in ordered_coverage
    ]
    figure, axis = plt.subplots(
        figsize=(7.2, max(3.2, 0.42 * len(order) + 1.25))
    )
    sns.barplot(
        data=frame,
        x="coverage",
        y="label",
        hue="stage",
        order=order,
        hue_order=[
            "Generation",
            "Capability success",
            "Security analyzer cohort",
        ],
        palette={
            "Generation": "#315c89",
            "Capability success": "#327a67",
            "Security analyzer cohort": "#c17a2b",
        },
        ax=axis,
    )
    for container in axis.containers:
        axis.bar_label(
            container,
            fmt=lambda value: f"{value:.0%}",
            padding=2,
            fontsize=6.3,
        )
    axis.set_xlim(0, 1.055)
    axis.xaxis.set_major_formatter(PercentFormatter(1.0))
    axis.set_xlabel("Share of planned generations")
    axis.set_ylabel("")
    axis.set_title(
        "Request-level coverage and conditional-security denominators",
        loc="left",
        pad=5,
    )
    axis.legend(
        frameon=False,
        ncol=3,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        columnspacing=1.2,
    )
    axis.grid(axis="x")
    axis.grid(axis="y", visible=False)
    sns.despine(ax=axis)
    figure.tight_layout(rect=(0, 0.07, 1, 1))
    return _save_figure(figure, output, "pipeline-coverage")


def _cwe_stratified_levels(cwe_rows: Sequence[dict[str, Any]]) -> list[str]:
    present = {str(row["treatment"]) for row in cwe_rows}
    return [level for level in CWE_STRATIFIED_LEVELS if level in present]


def _cwe_cell_denominators(
    row: dict[str, Any],
    field: str,
) -> tuple[int, int]:
    """Return eligible-generation denominators as Generic/treatment."""

    generic_field, treatment_field = CWE_DENOMINATOR_FIELDS[field]
    return int(row[generic_field]), int(row[treatment_field])


def plot_cwe_stratified_effects(
    cwe_rows: Sequence[dict[str, Any]],
    output: Path,
) -> list[str]:
    """Plot every task-matched lineage condition within each target CWE."""

    if not cwe_rows:
        return []
    models = sorted({str(row["model"]) for row in cwe_rows})
    row_keys = sorted(
        {
            (str(row["model"]), int(row["target_cwe"]))
            for row in cwe_rows
        },
        key=lambda value: (value[0], value[1]),
    )
    treatments = _cwe_stratified_levels(cwe_rows)
    if not treatments:
        return []
    lookup = {
        (
            str(row["model"]),
            int(row["target_cwe"]),
            str(row["treatment"]),
        ): row
        for row in cwe_rows
    }
    generic = str(cwe_rows[0]["generic"])
    labels = [
        (
            f"{model} · CWE-{target_cwe}"
            if len(models) > 1
            else f"CWE-{target_cwe}"
        )
        for model, target_cwe in row_keys
    ]
    panels = (
        ("capability_difference", "A  Functional\ncapability"),
        ("safety_difference", "B  Safety success\n(functional code)"),
        (
            "target_cwe_reduction",
            "C  Target-CWE finding reduction\n(functional code)",
        ),
    )
    figure, axes = plt.subplots(
        1,
        len(panels),
        figsize=(10.2, max(5.8, 0.39 * len(row_keys) + 2.1)),
        sharey=False,
    )
    color_map = sns.diverging_palette(28, 145, s=78, l=48, as_cmap=True)
    for panel_index, (axis, (field, title)) in enumerate(zip(axes, panels)):
        values = np.full((len(row_keys), len(treatments)), np.nan, dtype=float)
        available = np.zeros(values.shape, dtype=bool)
        generic_denominators = np.full(values.shape, -1, dtype=int)
        treatment_denominators = np.full(values.shape, -1, dtype=int)
        for row_index, (model, target_cwe) in enumerate(row_keys):
            for treatment_index, treatment in enumerate(treatments):
                row = lookup.get((model, target_cwe, treatment))
                if row is None:
                    continue
                available[row_index, treatment_index] = True
                values[row_index, treatment_index] = float(row[field])
                generic_n, treatment_n = _cwe_cell_denominators(row, field)
                generic_denominators[row_index, treatment_index] = generic_n
                treatment_denominators[row_index, treatment_index] = treatment_n
        finite = values[np.isfinite(values)]
        maximum = max((abs(float(value)) for value in finite), default=0.025)
        display_bound = max(0.025, math.ceil(maximum / 0.025) * 0.025)
        sns.heatmap(
            values,
            mask=~np.isfinite(values),
            ax=axis,
            cmap=color_map,
            center=0.0,
            vmin=-display_bound,
            vmax=display_bound,
            linewidths=0.45,
            linecolor="white",
            cbar=False,
        )
        axis.set_facecolor("#ecefeb")
        for row_index in range(len(row_keys)):
            for treatment_index in range(len(treatments)):
                value = values[row_index, treatment_index]
                generic_n = generic_denominators[row_index, treatment_index]
                treatment_n = treatment_denominators[row_index, treatment_index]
                low_denominator = (
                    available[row_index, treatment_index]
                    and min(generic_n, treatment_n)
                    < CWE_LOW_DENOMINATOR_THRESHOLD
                )
                if low_denominator:
                    axis.add_patch(
                        Rectangle(
                            (treatment_index, row_index),
                            1,
                            1,
                            facecolor="#d9ddda",
                            edgecolor="#78817c",
                            linewidth=0.45,
                            hatch="////",
                            zorder=2,
                        )
                    )
                if not available[row_index, treatment_index]:
                    annotation, color = "—", "#7b847f"
                elif not np.isfinite(value):
                    annotation = f"NA\nn={generic_n}/{treatment_n}"
                    color = "#17211c" if low_denominator else "#7b847f"
                else:
                    annotation = (
                        f"{value * 100:+.1f}\n"
                        f"n={generic_n}/{treatment_n}"
                    )
                    color = (
                        "#17211c"
                        if low_denominator
                        else "white"
                        if abs(float(value)) >= display_bound * 0.57
                        else "#17211c"
                    )
                axis.text(
                    treatment_index + 0.5,
                    row_index + 0.5,
                    annotation,
                    ha="center",
                    va="center",
                    fontsize=5.05,
                    color=color,
                    linespacing=0.9,
                    zorder=3,
                )
        axis.set_title(title, loc="left", pad=5)
        axis.set_xlabel("")
        axis.set_xticklabels(treatments, rotation=35, ha="right")
        if panel_index == 0:
            axis.set_yticks(np.arange(len(row_keys), dtype=float) + 0.5)
            axis.set_yticklabels(labels, rotation=0)
        else:
            axis.set_yticks(np.arange(len(row_keys), dtype=float) + 0.5)
            axis.set_yticklabels([])
        axis.set_ylabel("")
    figure.suptitle(
        f"CWE lineage performance relative to {generic}",
        x=0.06,
        y=0.995,
        ha="left",
        fontweight="bold",
    )
    figure.text(
        0.06,
        0.006,
        "Cell values are observed percentage-point improvements; positive (green) "
        "values favor the lineage condition. Each cell's second line is the number "
        "of eligible generations, n=Generic/condition.\nHatched gray cells have "
        f"min(n) < {CWE_LOW_DENOMINATOR_THRESHOLD}; the threshold is a visual "
        "caution, not an exclusion rule. — = level absent from the CWE lineage; "
        "NA = no estimable difference.\nSecurity outcomes are conditional on "
        "functional success. Descriptive task-matched summaries; color scales "
        "are panel-specific.",
        ha="left",
        va="bottom",
        fontsize=6.5,
    )
    figure.tight_layout(rect=(0, 0.145, 1, 0.965), w_pad=0.75)
    return _save_figure(figure, output, "cwe-stratified-effects")


def generate_figures(
    output: Path,
    descriptive: Sequence[dict[str, Any]],
    rows: Sequence[dict[str, Any]],
    model_rows: Sequence[dict[str, Any]],
    coverage: Sequence[dict[str, Any]],
    cwe_rows: Sequence[dict[str, Any]],
) -> list[str]:
    """Write every analysis figure through Seaborn/Matplotlib as PNG and PDF."""

    _plot_theme()
    for legacy in (
        "index.html",
        *(f"{stem}.svg" for stem in FIGURE_STEMS),
        "binary-improvements.svg",
        "binary-improvements.png",
        "binary-improvements.pdf",
    ):
        legacy_path = output / legacy
        if legacy_path.exists():
            legacy_path.unlink()
    filenames = []
    filenames.extend(plot_binary_distributions(descriptive, output))
    filenames.extend(plot_test_outcome_flow(rows, output))
    filenames.extend(plot_count_distribution(rows, output))
    filenames.extend(plot_improvements(model_rows, output, family="all"))
    filenames.extend(plot_improvements(model_rows, output, family="count"))
    filenames.extend(plot_coverage(coverage, output))
    filenames.extend(plot_cwe_stratified_effects(cwe_rows, output))
    return filenames


def fit_common_subset_models(
    rows: Sequence[dict[str, Any]],
    *,
    quadrature_points: int,
    overdispersion_threshold: float,
    ci_draws: int,
    seed: int,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[str],
    list[dict[str, Any]],
]:
    """Refit aggregate contrasts on tasks supporting Generic/Pillar/Class/Base."""

    common_rows = common_condition_subset(rows)
    model_rows: list[dict[str, Any]] = []
    matched_summaries: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    warnings: list[str] = []
    if not common_rows:
        return model_rows, matched_summaries, diagnostics, warnings, common_rows

    for outcome_index, outcome in enumerate(OUTCOMES):
        for contrast_index, (treatment, reference) in enumerate(
            COMMON_SUBSET_CONTRASTS
        ):
            selected, matched = matched_rows(
                common_rows,
                outcome,
                treatment,
                generic=reference,
            )
            matched_summaries.extend(
                {
                    "outcome": matched["outcome"],
                    "contrast": matched["contrast"],
                    "treatment": matched["treatment"],
                    **entry,
                }
                for entry in matched["models"]
            )
            label = f"common subset {outcome.name}/{treatment} vs {reference}"
            if not selected:
                warnings.append(f"{label}: sin observaciones elegibles")
                continue
            if {
                str(row["cwe_level"]) for row in selected
            } != {reference, treatment}:
                warnings.append(
                    f"{label}: sin observaciones elegibles en uno de los brazos"
                )
                continue
            if len({outcome.value(row) for row in selected}) < 2:
                warnings.append(f"{label}: resultado sin variación")
                continue

            family = outcome.family
            fit, fit_warnings = fit_mixed_glm(
                selected,
                outcome,
                treatment,
                generic=reference,
                family="poisson" if family == "count" else family,
                quadrature_points=quadrature_points,
            )
            dispersion = None
            if family == "count":
                dispersion = _poisson_dispersion(
                    fit, selected, outcome, treatment, reference
                )
                fit.dispersion = dispersion
                if dispersion > overdispersion_threshold:
                    fit, second_warnings = fit_mixed_glm(
                        selected,
                        outcome,
                        treatment,
                        generic=reference,
                        family="negative_binomial",
                        quadrature_points=quadrature_points,
                    )
                    fit.dispersion = dispersion
                    fit_warnings.extend(second_warnings)
            model_rows.extend(
                summarize_fit(
                    fit,
                    selected,
                    outcome,
                    treatment,
                    generic=reference,
                    ci_draws=ci_draws,
                    seed=seed + 10_000 + outcome_index * 100 + contrast_index,
                )
            )
            diagnostics.append(
                {
                    "outcome": outcome.name,
                    "contrast": f"{treatment} vs {reference}",
                    "family": fit.family,
                    "observations": fit.observations,
                    "tasks": fit.tasks,
                    "converged": fit.converged,
                    "log_likelihood": fit.log_likelihood,
                    "random_intercept_sd": fit.sigma,
                    "poisson_dispersion": dispersion,
                    "overdispersion_threshold": overdispersion_threshold,
                    "message": fit.message,
                    "warnings": " | ".join(fit_warnings),
                }
            )
            warnings.extend(f"{label}: {warning}" for warning in fit_warnings)

    apply_holm(model_rows, planned_comparisons=len(COMMON_SUBSET_CONTRASTS))
    return model_rows, matched_summaries, diagnostics, warnings, common_rows


MODEL_RESULT_FIELDS = (
    "outcome",
    "outcome_label",
    "family",
    "model",
    "contrast",
    "treatment",
    "generic",
    "tasks",
    "generic_n",
    "treatment_n",
    "generic_estimate",
    "generic_ci_low",
    "generic_ci_high",
    "treatment_estimate",
    "treatment_ci_low",
    "treatment_ci_high",
    "absolute_difference",
    "difference_ci_low",
    "difference_ci_high",
    "relative_measure",
    "relative_effect",
    "relative_ci_low",
    "relative_ci_high",
    "coefficient",
    "coefficient_se",
    "z_value",
    "p_value",
    "multiplicity_family",
    "multiplicity_planned_comparisons",
    "p_holm_within_outcome",
    "p_holm",
    "improvement",
    "improvement_ci_low",
    "improvement_ci_high",
)


def run_analysis(args: argparse.Namespace) -> dict[str, Any]:
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    raw_rows: list[dict[str, Any]] = []
    for path in args.results:
        raw_rows.extend(load_results(path))
    if not raw_rows:
        raise RuntimeError("No hay filas disponibles para analizar")
    rows = flatten_rows(raw_rows, analyzer_policy=args.analyzer_policy)
    generic = args.generic
    present_levels = {str(row["cwe_level"]) for row in rows}
    if generic not in present_levels:
        raise RuntimeError(f"No se encontró la condición de referencia {generic!r}")
    treatments = [
        level
        for level in LEVEL_ORDER
        if level != generic and level in present_levels
    ]
    treatments.extend(
        sorted(present_levels - set(LEVEL_ORDER) - {generic})
    )
    if not treatments:
        raise RuntimeError("No hay condiciones CWE-informed para comparar")

    coverage, statuses = coverage_statistics(rows)
    descriptive = descriptive_statistics(rows, treatments, generic=generic)
    cwe_descriptive = cwe_lineage_descriptive_statistics(
        rows,
        generic=generic,
        treatments=treatments,
    )
    target_distribution = target_abstraction_distribution(rows)
    matched_summaries: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    interaction_rows: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    warnings: list[str] = []
    for outcome_index, outcome in enumerate(OUTCOMES):
        for treatment_index, treatment in enumerate(treatments):
            selected, matched = matched_rows(
                rows, outcome, treatment, generic=generic
            )
            matched_summaries.extend(
                {
                    "outcome": matched["outcome"],
                    "contrast": matched["contrast"],
                    "treatment": matched["treatment"],
                    **entry,
                }
                for entry in matched["models"]
            )
            if not selected:
                warnings.append(f"{outcome.name}/{treatment}: sin observaciones elegibles")
                continue
            if {
                str(row["cwe_level"]) for row in selected
            } != {generic, treatment}:
                warnings.append(
                    f"{outcome.name}/{treatment}: sin observaciones elegibles "
                    "en uno de los brazos"
                )
                continue
            if len({outcome.value(row) for row in selected}) < 2:
                warnings.append(f"{outcome.name}/{treatment}: resultado sin variación")
                continue
            family = outcome.family
            fit, fit_warnings = fit_mixed_glm(
                selected,
                outcome,
                treatment,
                generic=generic,
                family="poisson" if family == "count" else family,
                quadrature_points=args.quadrature_points,
            )
            dispersion = None
            if family == "count":
                dispersion = _poisson_dispersion(
                    fit, selected, outcome, treatment, generic
                )
                fit.dispersion = dispersion
                if dispersion > args.overdispersion_threshold:
                    fit, second_warnings = fit_mixed_glm(
                        selected,
                        outcome,
                        treatment,
                        generic=generic,
                        family="negative_binomial",
                        quadrature_points=args.quadrature_points,
                    )
                    fit.dispersion = dispersion
                    fit_warnings.extend(second_warnings)
            seed = args.seed + outcome_index * 100 + treatment_index
            model_rows.extend(
                summarize_fit(
                    fit,
                    selected,
                    outcome,
                    treatment,
                    generic=generic,
                    ci_draws=args.ci_draws,
                    seed=seed,
                )
            )
            interaction_rows.extend(
                summarize_interactions(
                    fit,
                    selected,
                    outcome,
                    treatment,
                    generic=generic,
                )
            )
            diagnostics.append(
                {
                    "outcome": outcome.name,
                    "contrast": f"{treatment} vs {generic}",
                    "family": fit.family,
                    "observations": fit.observations,
                    "tasks": fit.tasks,
                    "converged": fit.converged,
                    "log_likelihood": fit.log_likelihood,
                    "random_intercept_sd": fit.sigma,
                    "poisson_dispersion": dispersion,
                    "overdispersion_threshold": args.overdispersion_threshold,
                    "message": fit.message,
                    "warnings": " | ".join(fit_warnings),
                }
            )
            warnings.extend(
                f"{outcome.name}/{treatment}: {warning}" for warning in fit_warnings
            )
    apply_holm(model_rows, planned_comparisons=len(treatments))
    apply_interaction_holm(
        interaction_rows,
        planned_comparisons=len(treatments),
    )
    (
        common_model_rows,
        common_matched_summaries,
        common_diagnostics,
        common_warnings,
        common_rows,
    ) = fit_common_subset_models(
        rows,
        quadrature_points=args.quadrature_points,
        overdispersion_threshold=args.overdispersion_threshold,
        ci_draws=args.ci_draws,
        seed=args.seed,
    )
    warnings.extend(common_warnings)

    _write_csv(output / "model_results.csv", model_rows, MODEL_RESULT_FIELDS)
    _write_csv(
        output / "interaction_tests.csv",
        interaction_rows,
        (
            "outcome",
            "contrast",
            "model",
            "reference_model",
            "coefficient",
            "coefficient_se",
            "z_value",
            "p_value",
            "p_holm",
        ),
    )
    _write_csv(
        output / "model_diagnostics.csv",
        diagnostics,
        (
            "outcome",
            "contrast",
            "family",
            "observations",
            "tasks",
            "converged",
            "log_likelihood",
            "random_intercept_sd",
            "poisson_dispersion",
            "overdispersion_threshold",
            "message",
            "warnings",
        ),
    )
    _write_csv(
        output / "common_subset_model_results.csv",
        common_model_rows,
        MODEL_RESULT_FIELDS,
    )
    _write_csv(
        output / "common_subset_model_diagnostics.csv",
        common_diagnostics,
        (
            "outcome",
            "contrast",
            "family",
            "observations",
            "tasks",
            "converged",
            "log_likelihood",
            "random_intercept_sd",
            "poisson_dispersion",
            "overdispersion_threshold",
            "message",
            "warnings",
        ),
    )
    _write_csv(
        output / "common_subset_matched_cohorts.csv",
        common_matched_summaries,
        (
            "outcome",
            "contrast",
            "treatment",
            "model",
            "generic_supported_tasks",
            "treatment_supported_tasks",
            "matched_tasks",
            "generic_observations",
            "treatment_observations",
        ),
    )
    _write_csv(
        output / "matched_cohorts.csv",
        matched_summaries,
        (
            "outcome",
            "contrast",
            "treatment",
            "model",
            "generic_supported_tasks",
            "treatment_supported_tasks",
            "matched_tasks",
            "generic_observations",
            "treatment_observations",
        ),
    )
    _write_csv(
        output / "descriptive_statistics.csv",
        descriptive,
        (
            "outcome",
            "outcome_label",
            "model",
            "condition",
            "tasks",
            "observations",
            "events",
            "mean",
            "standard_deviation",
            "q1",
            "median",
            "q3",
            "minimum",
            "maximum",
        ),
    )
    _write_csv(
        output / "coverage.csv",
        coverage,
        (
            "model",
            "condition",
            "rows",
            "tasks",
            "generation_success",
            "generation_failures",
            "evaluation_observed",
            "evaluation_failures",
            "capability_success",
            "safety_observed",
            "analyzer_observed",
            "security_analyzer_cohort",
        ),
    )
    _write_csv(
        output / "cwe_descriptive_statistics.csv",
        cwe_descriptive,
        (
            "model",
            "target_cwe",
            "generic",
            "treatment",
            "matched_tasks",
            "generic_capability_n",
            "generic_capability_events",
            "generic_capability_rate",
            "treatment_capability_n",
            "treatment_capability_events",
            "treatment_capability_rate",
            "capability_difference",
            "generic_safety_n",
            "generic_safety_events",
            "generic_safety_rate",
            "treatment_safety_n",
            "treatment_safety_events",
            "treatment_safety_rate",
            "safety_difference",
            "generic_target_cwe_n",
            "generic_target_cwe_events",
            "generic_target_cwe_rate",
            "treatment_target_cwe_n",
            "treatment_target_cwe_events",
            "treatment_target_cwe_rate",
            "target_cwe_reduction",
        ),
    )
    _write_csv(
        output / "status_counts.csv",
        statuses,
        ("model", "condition", "stage", "status", "count"),
    )
    _write_csv(
        output / "target_abstraction_distribution.csv",
        target_distribution,
        ("target_abstraction", "tasks", "percentage"),
    )

    figures = generate_figures(
        output,
        descriptive,
        rows,
        model_rows,
        coverage,
        cwe_descriptive,
    )
    summary = {
        "results": [str(path) for path in args.results],
        "output_directory": str(output),
        "rows": len(rows),
        "tasks": len({row["task_id"] for row in rows}),
        "models": len({row["model"] for row in rows}),
        "conditions": [generic, *treatments],
        "generic": generic,
        "analyzer_policy": args.analyzer_policy,
        "overdispersion_threshold": args.overdispersion_threshold,
        "quadrature_points": args.quadrature_points,
        "ci_draws": args.ci_draws,
        "holm_families": (
            "overall and capability outcomes: five planned level contrasts each; "
            "conditional-security family: four outcomes by five levels "
            "(20 planned contrasts)"
        ),
        "capability_estimand": (
            "strict request-level success; invalid or missing generations count as failures"
        ),
        "security_estimand": (
            "safety tests and analyzer outcomes conditional on capability-test success"
        ),
        "cwe_figure_contrast": (
            f"Pillar, Class, and Base vs {generic}; descriptive task-matched "
            "differences; Variant and Compound retained in the CSV only"
        ),
        "cwe_figure_denominators": (
            "each cell is annotated n=Generic/condition; cells with either "
            f"eligible denominator below {CWE_LOW_DENOMINATOR_THRESHOLD} are "
            "gray and hatched without being excluded"
        ),
        "target_abstraction_distribution": target_distribution,
        "common_subset": {
            "conditions": list(COMMON_SUBSET_CONDITIONS),
            "contrasts": [
                f"{treatment} vs {reference}"
                for treatment, reference in COMMON_SUBSET_CONTRASTS
            ],
            "tasks": len({row["task_id"] for row in common_rows}),
            "tasks_by_model": {
                model: len(
                    {
                        row["task_id"]
                        for row in common_rows
                        if str(row["model"]) == model
                    }
                )
                for model in sorted({str(row["model"]) for row in common_rows})
            },
            "rows": len(common_rows),
            "model_results": len(common_model_rows),
            "holm_families": (
                "overall and capability outcomes: four common-subset contrasts each; "
                "conditional-security family: four outcomes by four contrasts "
                "(16 planned contrasts)"
            ),
        },
        "estimated_scale": "conditional response scale at random intercept zero (typical task)",
        "confidence_intervals": "95% pointwise parameter-simulation intervals; Holm correction applies to p-values",
        "model_results": len(model_rows),
        "interaction_tests": len(interaction_rows),
        "figure_backend": "seaborn + matplotlib",
        "figures": figures,
        "warnings": warnings,
    }
    (output / "analysis_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results",
        type=Path,
        action="append",
        required=True,
        help="results.parquet, directorio de ejecución o directorio checkpoints; repetible",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--generic", default="Generic")
    parser.add_argument(
        "--analyzer-policy",
        choices=("any", "all"),
        default="any",
        help="any: al menos un analizador completo; all: Bandit y CodeQL completos",
    )
    parser.add_argument("--overdispersion-threshold", type=float, default=1.2)
    parser.add_argument("--quadrature-points", type=int, default=15)
    parser.add_argument("--ci-draws", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260723)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.quadrature_points < 5:
        raise SystemExit("--quadrature-points debe ser al menos 5")
    if args.ci_draws < 200:
        raise SystemExit("--ci-draws debe ser al menos 200")
    if args.overdispersion_threshold <= 1.0:
        raise SystemExit("--overdispersion-threshold debe ser mayor que 1")
    summary = run_analysis(args)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
