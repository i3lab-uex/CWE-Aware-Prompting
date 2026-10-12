from __future__ import annotations

from statistical_analysis import (
    OUTCOMES,
    _cwe_cell_denominators,
    _cwe_stratified_levels,
    apply_holm,
    common_condition_subset,
    coverage_statistics,
    cwe_descriptive_statistics,
    cwe_lineage_descriptive_statistics,
    descriptive_statistics,
    fit_mixed_glm,
    flatten_rows,
    generate_figures,
    holm_adjust,
    matched_rows,
    summarize_fit,
    summarize_interactions,
    target_abstraction_distribution,
)
from sample_checkpoint_evaluation import reset_downstream_results, select_matched_rows


def raw_row(
    task: str,
    condition: str,
    generation: int,
    *,
    passed: bool,
    target_finding: bool = False,
    other_finding: bool = False,
) -> dict:
    findings = []
    if target_finding:
        findings.append({"cwe": 78, "rule": "target"})
    if other_finding:
        findings.append({"cwe": 20, "rule": "other"})
    return {
        "task_id": task,
        "target_cwe": 78,
        "cwe_level": condition,
        "generation_index": generation,
        "model": "synthetic",
        "generation_status": "ok",
        "evaluation_status": "complete",
        "all_tests_pass": passed,
        "capability_total": 1,
        "capability_passed": int(passed),
        "safety_total": 1,
        "safety_passed": int(passed),
        "bandit_status": "complete",
        "codeql_status": "unavailable",
        "bandit_findings": findings,
        "codeql_findings": [],
    }


def test_flatten_rows_counts_target_and_other_findings() -> None:
    row = raw_row(
        "task",
        "Generic",
        0,
        passed=True,
        target_finding=True,
        other_finding=True,
    )

    flattened = flatten_rows([row], analyzer_policy="any")[0]

    assert flattened["analyzer_observed"] is True
    assert flattened["finding_count"] == 2
    assert flattened["target_finding_count"] == 1
    assert flattened["other_finding_count"] == 1
    assert flatten_rows([row], analyzer_policy="all")[0]["analyzer_observed"] is False


def test_test_outcomes_separate_overall_capability_and_safety_success() -> None:
    row = raw_row("task", "Generic", 0, passed=False)
    row.update(
        all_tests_pass=False,
        capability_total=2,
        capability_passed=2,
        safety_total=1,
        safety_passed=0,
    )
    outcomes = {outcome.name: outcome for outcome in OUTCOMES}

    assert outcomes["overall_test_success"].value(row) == 0.0
    assert outcomes["capability_test_success"].value(row) == 1.0
    assert outcomes["safety_test_success"].value(row) == 0.0


def test_capability_counts_invalid_responses_as_failures() -> None:
    row = raw_row("task", "Generic", 0, passed=False)
    row.update(
        generation_status="error",
        evaluation_status="skipped_generation_error",
        capability_total=0,
        capability_passed=0,
    )
    capability = next(
        outcome for outcome in OUTCOMES
        if outcome.name == "capability_test_success"
    )

    assert capability.eligible(row) is True
    assert capability.value(row) == 0.0


def test_security_outcomes_require_capability_success() -> None:
    row = raw_row(
        "task",
        "Generic",
        0,
        passed=False,
        target_finding=True,
        other_finding=True,
    )
    flattened = flatten_rows([row], analyzer_policy="any")[0]
    security = {
        outcome.name: outcome
        for outcome in OUTCOMES
        if outcome.name in {
            "safety_test_success",
            "target_cwe_present",
            "other_cwe_present",
            "finding_count",
        }
    }

    assert not any(outcome.eligible(flattened) for outcome in security.values())

    flattened.update(
        capability_total=1,
        capability_passed=1,
        safety_total=1,
        safety_passed=0,
    )
    assert all(outcome.eligible(flattened) for outcome in security.values())
    assert security["safety_test_success"].value(flattened) == 0.0


def test_matching_uses_only_tasks_supporting_both_conditions() -> None:
    rows = flatten_rows(
        [
            raw_row("matched", "Generic", 0, passed=False),
            raw_row("matched", "Pillar", 0, passed=True),
            raw_row("generic-only", "Generic", 0, passed=True),
        ],
        analyzer_policy="any",
    )

    selected, summary = matched_rows(
        rows,
        OUTCOMES[0],
        "Pillar",
        generic="Generic",
    )

    assert {row["task_id"] for row in selected} == {"matched"}
    assert summary["models"][0]["matched_tasks"] == 1
    assert summary["models"][0]["generic_supported_tasks"] == 2


def test_common_subset_requires_all_four_conditions_and_drops_other_levels() -> None:
    raw = []
    for condition in ("Generic", "Pillar", "Class", "Base", "Variant"):
        raw.append(raw_row("complete", condition, 0, passed=True))
    for condition in ("Generic", "Pillar", "Class"):
        raw.append(raw_row("missing-base", condition, 0, passed=True))
    rows = flatten_rows(raw, analyzer_policy="any")

    selected = common_condition_subset(rows)

    assert {row["task_id"] for row in selected} == {"complete"}
    assert {row["cwe_level"] for row in selected} == {
        "Generic",
        "Pillar",
        "Class",
        "Base",
    }


def test_target_abstraction_distribution_uses_the_target_prompt_node() -> None:
    rows = []
    for task, level in (
        ("base-1", "Base"),
        ("base-2", "Base"),
        ("class", "Class"),
        ("variant", "Variant"),
        ("compound", "Compound"),
    ):
        row = raw_row(task, level, 0, passed=True)
        row["prompt_cwe"] = row["target_cwe"]
        rows.append(row)
    # An ancestor prompt is not the target abstraction and must not be counted.
    ancestor = raw_row("base-1", "Class", 0, passed=True)
    ancestor["prompt_cwe"] = 77
    rows.append(ancestor)

    distribution = target_abstraction_distribution(rows)

    assert [(row["target_abstraction"], row["tasks"]) for row in distribution] == [
        ("Base", 2),
        ("Class", 1),
        ("Variant", 1),
        ("Compound", 1),
    ]
    assert sum(row["percentage"] for row in distribution) == 1.0


def test_holm_adjustment_is_step_down_and_monotone() -> None:
    assert holm_adjust([0.01, 0.04, 0.03]) == [0.03, 0.06, 0.06]


def test_security_holm_family_spans_four_outcomes_and_five_levels() -> None:
    rows = [
        {"outcome": "safety_test_success", "model": "m", "p_value": 0.01},
        {"outcome": "overall_test_success", "model": "m", "p_value": 0.01},
    ]

    apply_holm(rows, planned_comparisons=5)

    assert rows[0]["multiplicity_family"] == "security_conditional"
    assert rows[0]["multiplicity_planned_comparisons"] == 20
    assert rows[0]["p_holm_within_outcome"] == 0.05
    assert rows[0]["p_holm"] == 0.2
    assert rows[1]["multiplicity_planned_comparisons"] == 5
    assert rows[1]["p_holm"] == 0.05


def test_binomial_random_intercept_model_retains_repeated_observations() -> None:
    raw = []
    for task_index in range(12):
        for generation in range(5):
            raw.append(
                raw_row(
                    f"task-{task_index}",
                    "Generic",
                    generation,
                    passed=(generation + task_index) % 5 < 2,
                )
            )
            raw.append(
                raw_row(
                    f"task-{task_index}",
                    "Pillar",
                    generation,
                    passed=(generation + task_index) % 5 < 3,
                )
            )
    rows = flatten_rows(raw, analyzer_policy="any")
    fit, warnings = fit_mixed_glm(
        rows,
        OUTCOMES[0],
        "Pillar",
        generic="Generic",
        family="binomial",
        quadrature_points=9,
    )
    summary = summarize_fit(
        fit,
        rows,
        OUTCOMES[0],
        "Pillar",
        generic="Generic",
        ci_draws=250,
        seed=7,
    )

    assert fit.observations == 120
    assert fit.tasks == 12
    assert fit.converged, warnings
    assert summary[0]["treatment_estimate"] > summary[0]["generic_estimate"]
    assert summary[0]["absolute_difference"] > 0


def test_multiple_models_add_a_condition_by_model_interaction() -> None:
    raw = []
    for model, treatment_threshold in (("small", 3), ("large", 4)):
        for task_index in range(10):
            for generation in range(5):
                generic = raw_row(
                    f"task-{task_index}",
                    "Generic",
                    generation,
                    passed=(generation + task_index) % 5 < 2,
                )
                generic["model"] = model
                treatment = raw_row(
                    f"task-{task_index}",
                    "Pillar",
                    generation,
                    passed=(generation + task_index) % 5 < treatment_threshold,
                )
                treatment["model"] = model
                raw.extend((generic, treatment))
    rows = flatten_rows(raw, analyzer_policy="any")
    fit, warnings = fit_mixed_glm(
        rows,
        OUTCOMES[0],
        "Pillar",
        generic="Generic",
        family="binomial",
        quadrature_points=9,
    )
    interactions = summarize_interactions(
        fit,
        rows,
        OUTCOMES[0],
        "Pillar",
        generic="Generic",
    )

    assert fit.converged, warnings
    assert len(interactions) == 1
    assert interactions[0]["model"] == "small"
    assert interactions[0]["reference_model"] == "large"


def test_negative_binomial_mixed_model_handles_overdispersed_counts() -> None:
    raw = []
    for task_index in range(10):
        for condition, counts in (
            ("Generic", (0, 0, 1, 5, 10)),
            ("Pillar", (0, 0, 1, 2, 6)),
        ):
            for generation, count in enumerate(counts):
                row = raw_row(
                    f"task-{task_index}",
                    condition,
                    generation,
                    passed=True,
                )
                row["bandit_findings"] = [{"cwe": 20} for _ in range(count)]
                raw.append(row)
    rows = flatten_rows(raw, analyzer_policy="any")

    fit, warnings = fit_mixed_glm(
        rows,
        OUTCOMES[-1],
        "Pillar",
        generic="Generic",
        family="negative_binomial",
        quadrature_points=9,
    )

    assert fit.converged, warnings
    assert fit.family == "negative_binomial"
    assert len(fit.parameters) == len(fit.fixed_names) + 2


def test_checkpoint_sample_is_exact_disjoint_and_matched() -> None:
    raw = []
    for task_index in range(8):
        for condition in ("Generic", "Pillar", "Class"):
            for generation in range(5):
                raw.append(
                    raw_row(
                        f"task-{task_index}",
                        condition,
                        generation,
                        passed=True,
                    )
                )

    sampled, selection = select_matched_rows(
        raw,
        sample_size=40,
        repetitions=5,
        seed=11,
    )

    assert len(sampled) == 40
    assert len(selection) == 4
    assert len({item["task_id"] for item in selection}) == 4
    for item in selection:
        task_rows = [row for row in sampled if row["task_id"] == item["task_id"]]
        assert {row["cwe_level"] for row in task_rows} == {
            "Generic",
            item["treatment"],
        }
        assert len(task_rows) == 10


def test_checkpoint_sample_resets_existing_evaluation_and_analyzers() -> None:
    rows = [
        {
            "generation_status": "ok",
            "evaluation_status": "complete",
            "evaluation_error": "old",
            "all_tests_pass": True,
            "test_results": [{"passed": True}],
            "bandit_status": "complete",
            "bandit_findings": [{"cwe": 78}],
            "codeql_status": "complete",
            "codeql_findings": [{"cwe": 78}],
        },
        {
            "generation_status": "error",
            "evaluation_status": "runtime_error",
            "bandit_status": "complete",
            "codeql_status": "complete",
        },
    ]

    reset_downstream_results(rows)

    assert rows[0]["evaluation_status"] == "pending"
    assert rows[0]["bandit_status"] == "pending"
    assert rows[0]["codeql_status"] == "pending"
    assert rows[0]["all_tests_pass"] is False
    assert rows[0]["test_results"] == []
    assert rows[0]["bandit_findings"] == []
    assert rows[1]["evaluation_status"] == "skipped_generation_error"
    assert rows[1]["bandit_status"] == "skipped_generation_error"
    assert rows[1]["codeql_status"] == "skipped_generation_error"


def test_cwe_descriptives_match_tasks_and_condition_security_on_capability() -> None:
    raw = [
        raw_row(
            "task",
            "Generic",
            0,
            passed=True,
            target_finding=True,
        ),
        raw_row("task", "Generic", 1, passed=False),
        raw_row("task", "Class", 0, passed=True),
        raw_row("task", "Class", 1, passed=True),
    ]
    rows = flatten_rows(raw, analyzer_policy="any")

    summaries = cwe_descriptive_statistics(
        rows,
        generic="Generic",
        treatment="Class",
    )

    assert len(summaries) == 1
    summary = summaries[0]
    assert summary["target_cwe"] == 78
    assert summary["matched_tasks"] == 1
    assert summary["capability_difference"] == 0.5
    assert summary["generic_safety_n"] == 1
    assert summary["treatment_safety_n"] == 2
    assert summary["safety_difference"] == 0.0
    assert summary["target_cwe_reduction"] == 1.0


def test_cwe_lineage_descriptives_include_every_available_condition() -> None:
    raw = [
        raw_row("task", "Generic", 0, passed=False),
        raw_row("task", "Pillar", 0, passed=True),
        raw_row("task", "Class", 0, passed=False),
    ]
    rows = flatten_rows(raw, analyzer_policy="any")

    summaries = cwe_lineage_descriptive_statistics(
        rows,
        generic="Generic",
        treatments=["Pillar", "Class", "Base"],
    )

    assert [summary["treatment"] for summary in summaries] == ["Pillar", "Class"]
    assert summaries[0]["capability_difference"] == 1.0
    assert summaries[1]["capability_difference"] == 0.0


def test_cwe_stratified_figure_excludes_variant_and_compound() -> None:
    rows = [
        {"treatment": level}
        for level in ("Pillar", "Class", "Base", "Variant", "Compound")
    ]

    assert _cwe_stratified_levels(rows) == ["Pillar", "Class", "Base"]


def test_cwe_figure_uses_outcome_specific_paired_denominators() -> None:
    row = {
        "generic_capability_n": 255,
        "treatment_capability_n": 250,
        "generic_safety_n": 7,
        "treatment_safety_n": 5,
        "generic_target_cwe_n": 6,
        "treatment_target_cwe_n": 4,
    }

    assert _cwe_cell_denominators(row, "capability_difference") == (255, 250)
    assert _cwe_cell_denominators(row, "safety_difference") == (7, 5)
    assert _cwe_cell_denominators(row, "target_cwe_reduction") == (6, 4)


def test_figures_use_static_seaborn_matplotlib_outputs(tmp_path) -> None:
    raw = []
    for condition in ("Generic", "Pillar", "Class"):
        for generation in range(5):
            raw.append(
                raw_row(
                    "task",
                    condition,
                    generation,
                    passed=generation < (2 if condition == "Generic" else 3),
                    other_finding=generation == 0,
                )
            )
    rows = flatten_rows(raw, analyzer_policy="any")
    descriptive = descriptive_statistics(
        rows,
        ["Pillar", "Class"],
        generic="Generic",
    )
    cwe_descriptive = cwe_lineage_descriptive_statistics(
        rows,
        generic="Generic",
        treatments=["Pillar", "Class"],
    )
    coverage, _ = coverage_statistics(rows)
    model_rows = [
        {
            "outcome": "overall_test_success",
            "outcome_label": "All-test success (capability + safety)",
            "model": "synthetic",
            "treatment": "Pillar",
            "improvement": 0.1,
            "improvement_ci_low": -0.02,
            "improvement_ci_high": 0.22,
            "relative_effect": 1.2,
            "relative_ci_low": 0.9,
            "relative_ci_high": 1.5,
            "p_holm": 0.08,
        },
        {
            "outcome": "finding_count",
            "outcome_label": "Analyzer finding count",
            "model": "synthetic",
            "treatment": "Pillar",
            "improvement": 0.15,
            "improvement_ci_low": 0.03,
            "improvement_ci_high": 0.27,
            "relative_effect": 0.82,
            "relative_ci_low": 0.71,
            "relative_ci_high": 0.95,
            "p_holm": 0.02,
        },
    ]
    (tmp_path / "index.html").write_text("legacy", encoding="utf-8")
    (tmp_path / "binary-improvements.svg").write_text("legacy", encoding="utf-8")
    (tmp_path / "binary-improvements.png").write_text("legacy", encoding="utf-8")
    (tmp_path / "binary-improvements.pdf").write_text("legacy", encoding="utf-8")

    filenames = generate_figures(
        tmp_path,
        descriptive,
        rows,
        model_rows,
        coverage,
        cwe_descriptive,
    )

    assert len(filenames) == 14
    assert "adjusted-effects.png" in filenames
    assert "adjusted-effects.pdf" in filenames
    assert "test-outcome-flow.png" in filenames
    assert "test-outcome-flow.pdf" in filenames
    assert "cwe-stratified-effects.png" in filenames
    assert "cwe-stratified-effects.pdf" in filenames
    assert {path.suffix for path in map(tmp_path.joinpath, filenames)} == {
        ".png",
        ".pdf",
    }
    assert all((tmp_path / filename).stat().st_size > 0 for filename in filenames)
    assert not list(tmp_path.glob("binary-improvements.*"))
    assert not list(tmp_path.glob("*.html"))
    assert not list(tmp_path.glob("*.svg"))
