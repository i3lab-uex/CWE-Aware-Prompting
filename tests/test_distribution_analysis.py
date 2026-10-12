import csv
import json
from pathlib import Path

from analyze_distribution import build_distribution_report
from cwe_experiment.dataset import DEFAULT_DATASET_PATH


def test_distribution_report_matches_experimental_design(tmp_path: Path) -> None:
    summary = build_distribution_report(DEFAULT_DATASET_PATH, tmp_path, n=3)

    assert summary["total_samples"] == 1345
    assert summary["functional_samples"] == 819
    assert summary["excluded_without_tests"] == 526
    assert summary["target_cwes"] == 17
    assert summary["prompt_conditions"] == 3023
    assert summary["projected_generations"] == 9069
    selection = summary["selection_composition"]
    assert selection["original_target_cwes"] == 27
    assert selection["retained_target_cwes"] == 17
    assert selection["entirely_excluded_target_cwes"] == 10
    assert selection["mixed_selection_target_cwes"] == 0
    assert selection["maximum_absolute_percentage_point_shift"] == 11.278

    stored = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert stored["n"] == 3
    with (tmp_path / "levels.csv").open(encoding="utf-8") as handle:
        levels = {row["level"]: int(row["samples"]) for row in csv.DictReader(handle)}
    assert levels == {
        "Generic": 819,
        "Pillar": 819,
        "Class": 819,
        "Base": 475,
        "Variant": 51,
        "Compound": 40,
    }
    with (tmp_path / "selection_by_target_abstraction.csv").open(
        encoding="utf-8"
    ) as handle:
        selection_levels = {
            row["target_abstraction"]: (
                int(row["original_tasks"]),
                int(row["retained_tasks"]),
                int(row["excluded_tasks"]),
            )
            for row in csv.DictReader(handle)
        }
    assert selection_levels == {
        "Base": (848, 424, 424),
        "Class": (406, 304, 102),
        "Variant": (51, 51, 0),
        "Compound": (40, 40, 0),
    }
    with (tmp_path / "selection_by_target_cwe.csv").open(
        encoding="utf-8"
    ) as handle:
        selection_cwes = list(csv.DictReader(handle))
    assert len(selection_cwes) == 27
    assert sum(
        row["selection_status"] == "excluded_all" for row in selection_cwes
    ) == 10
    assert not any(row["selection_status"] == "mixed" for row in selection_cwes)

    stems = {
        "dataset_coverage",
        "samples_by_cwe",
        "levels",
        "cwe_level_matrix",
        "condition_patterns",
        "prompt_lengths",
    }
    expected = {
        f"{stem}.{extension}"
        for stem in stems
        for extension in ("png", "pdf")
    }
    assert expected <= {path.name for path in tmp_path.iterdir()}
    assert all((tmp_path / filename).stat().st_size > 0 for filename in expected)
    assert stored["figure_backend"] == "seaborn + matplotlib"
    assert not list(tmp_path.glob("*.html"))
    assert not list(tmp_path.glob("*.svg"))


def test_distribution_report_rejects_non_positive_n(tmp_path: Path) -> None:
    try:
        build_distribution_report(DEFAULT_DATASET_PATH, tmp_path, n=0)
    except ValueError as exc:
        assert "n" in str(exc)
    else:
        raise AssertionError("n=0 must be rejected")
