"""Analyze the experimental dataset and create publication-friendly figures."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import json
import math
from pathlib import Path
from statistics import mean
from typing import Any, Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import pandas as pd
from scipy.stats import chi2_contingency
import seaborn as sns

from cwe_experiment.dataset import (
    DEFAULT_DATASET_PATH,
    _field,
    _read_rows,
    load_samples,
)
from cwe_experiment.prompts import build_prompt_conditions
from utils.cwe_hierarchy import get_canonical_lineage


LEVEL_ORDER = ("Generic", "Pillar", "Class", "Base", "Variant", "Compound")
TARGET_ABSTRACTION_ORDER = ("Base", "Class", "Variant", "Compound")
COLORS = {
    "Generic": "#52616b",
    "Pillar": "#315c89",
    "Class": "#327a67",
    "Base": "#c17a2b",
    "Variant": "#9b4f68",
    "Compound": "#73559b",
}


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _quantile(values: list[int], fraction: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def dataset_selection_distributions(
    dataset: str | Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Compare target-CWE composition before and after the functional-test filter."""

    rows = _read_rows(Path(dataset))
    abstraction_by_cwe: dict[int, str] = {}
    total_by_level: Counter[str] = Counter()
    retained_by_level: Counter[str] = Counter()
    excluded_by_level: Counter[str] = Counter()
    total_by_cwe: Counter[int] = Counter()
    retained_by_cwe: Counter[int] = Counter()
    excluded_by_cwe: Counter[int] = Counter()

    for row in rows:
        target_cwe = int(row["CWE_ID"])
        lineage = get_canonical_lineage(target_cwe)
        target_abstraction = str(lineage[-1]["abstraction"])
        previous = abstraction_by_cwe.setdefault(target_cwe, target_abstraction)
        if previous != target_abstraction:
            raise RuntimeError(
                f"CWE-{target_cwe} tiene una abstracción objetivo inconsistente"
            )
        retained = bool(str(_field(row, "unittest.testcases") or "").strip())
        total_by_level[target_abstraction] += 1
        total_by_cwe[target_cwe] += 1
        if retained:
            retained_by_level[target_abstraction] += 1
            retained_by_cwe[target_cwe] += 1
        else:
            excluded_by_level[target_abstraction] += 1
            excluded_by_cwe[target_cwe] += 1

    total = len(rows)
    retained_total = sum(retained_by_level.values())
    excluded_total = sum(excluded_by_level.values())
    present_levels = set(total_by_level)
    ordered_levels = [
        level for level in TARGET_ABSTRACTION_ORDER if level in present_levels
    ]
    ordered_levels.extend(sorted(present_levels - set(TARGET_ABSTRACTION_ORDER)))
    level_rows = []
    for level in ordered_levels:
        level_total = total_by_level[level]
        retained = retained_by_level[level]
        excluded = excluded_by_level[level]
        original_percentage = 100 * level_total / total
        retained_percentage = 100 * retained / retained_total
        level_rows.append(
            {
                "target_abstraction": level,
                "original_tasks": level_total,
                "original_percentage": round(original_percentage, 3),
                "retained_tasks": retained,
                "retained_percentage": round(retained_percentage, 3),
                "excluded_tasks": excluded,
                "excluded_percentage": round(100 * excluded / excluded_total, 3),
                "retention_rate": round(100 * retained / level_total, 3),
                "retained_minus_original_percentage_points": round(
                    retained_percentage - original_percentage,
                    3,
                ),
            }
        )

    cwe_rows = []
    for target_cwe in sorted(total_by_cwe):
        cwe_total = total_by_cwe[target_cwe]
        retained = retained_by_cwe[target_cwe]
        excluded = excluded_by_cwe[target_cwe]
        status = (
            "retained_all"
            if retained == cwe_total
            else "excluded_all"
            if excluded == cwe_total
            else "mixed"
        )
        cwe_rows.append(
            {
                "target_cwe": target_cwe,
                "target_abstraction": abstraction_by_cwe[target_cwe],
                "original_tasks": cwe_total,
                "original_percentage": round(100 * cwe_total / total, 3),
                "retained_tasks": retained,
                "retained_percentage": round(
                    100 * retained / retained_total,
                    3,
                ),
                "excluded_tasks": excluded,
                "excluded_percentage": round(
                    100 * excluded / excluded_total,
                    3,
                ),
                "retention_rate": round(100 * retained / cwe_total, 3),
                "selection_status": status,
            }
        )

    contingency = [
        [retained_by_level[level], excluded_by_level[level]]
        for level in ordered_levels
    ]
    chi_square, p_value, degrees_of_freedom, _ = chi2_contingency(contingency)
    selection_summary = {
        "original_tasks": total,
        "retained_tasks": retained_total,
        "excluded_tasks": excluded_total,
        "original_target_cwes": len(total_by_cwe),
        "retained_target_cwes": sum(
            bool(retained_by_cwe[cwe]) for cwe in total_by_cwe
        ),
        "entirely_excluded_target_cwes": sum(
            retained_by_cwe[cwe] == 0 for cwe in total_by_cwe
        ),
        "mixed_selection_target_cwes": sum(
            retained_by_cwe[cwe] > 0 and excluded_by_cwe[cwe] > 0
            for cwe in total_by_cwe
        ),
        "abstraction_selection_chi_square": float(chi_square),
        "abstraction_selection_degrees_of_freedom": int(degrees_of_freedom),
        "abstraction_selection_p_value": float(p_value),
        "abstraction_selection_cramers_v": math.sqrt(float(chi_square) / total),
        "maximum_absolute_percentage_point_shift": max(
            abs(float(row["retained_minus_original_percentage_points"]))
            for row in level_rows
        ),
    }
    return level_rows, cwe_rows, selection_summary


DISTRIBUTION_FIGURE_STEMS = (
    "dataset_coverage",
    "samples_by_cwe",
    "levels",
    "cwe_level_matrix",
    "condition_patterns",
    "prompt_lengths",
)


def _plot_theme() -> None:
    sns.set_theme(
        context="paper",
        style="whitegrid",
        font_scale=1.05,
        rc={
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "grid.color": "#e2e7e4",
            "grid.linewidth": 0.7,
            "axes.titleweight": "bold",
        },
    )


def _save_figure(figure: plt.Figure, output: Path, stem: str) -> list[str]:
    filenames = []
    for extension, options in (("png", {"dpi": 300}), ("pdf", {})):
        filename = f"{stem}.{extension}"
        figure.savefig(
            output / filename,
            bbox_inches="tight",
            facecolor="white",
            **options,
        )
        filenames.append(filename)
    plt.close(figure)
    return filenames


def _plot_coverage(
    output: Path,
    total: int,
    functional: int,
    excluded: int,
) -> list[str]:
    figure, axis = plt.subplots(figsize=(9, 2.6))
    fractions = [functional / total, excluded / total]
    labels = ["Con tests", "Sin tests"]
    colors = ["#327a67", "#d9dedb"]
    left = 0.0
    for fraction, label, color, count in zip(
        fractions,
        labels,
        colors,
        (functional, excluded),
    ):
        axis.barh(["Dataset"], [fraction], left=left, color=color, label=label)
        axis.text(
            left + fraction / 2,
            0,
            f"{label}: {count:,} ({fraction:.1%})",
            ha="center",
            va="center",
            fontsize=9,
        )
        left += fraction
    axis.set_xlim(0, 1)
    axis.xaxis.set_major_formatter(PercentFormatter(1.0))
    axis.set_xlabel(f"Proporción de {total:,} muestras")
    axis.set_ylabel("")
    axis.set_title("Cobertura funcional del dataset", loc="left")
    axis.legend(frameon=False, ncol=2, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    figure.tight_layout()
    return _save_figure(figure, output, "dataset_coverage")


def _plot_horizontal_bars(
    output: Path,
    stem: str,
    title: str,
    rows: Iterable[tuple[str, int]],
    *,
    color: str,
) -> list[str]:
    frame = pd.DataFrame(list(rows), columns=["label", "value"])
    figure, axis = plt.subplots(figsize=(9.5, max(3.2, 0.42 * len(frame) + 1.5)))
    sns.barplot(data=frame, x="value", y="label", color=color, ax=axis)
    for container in axis.containers:
        axis.bar_label(container, fmt=lambda value: f"{value:,.0f}", padding=3, fontsize=8)
    axis.set_xlabel("Muestras")
    axis.set_ylabel("")
    axis.set_title(title, loc="left")
    figure.tight_layout()
    return _save_figure(figure, output, stem)


def _plot_levels(
    output: Path,
    level_rows: list[dict[str, Any]],
    total_samples: int,
) -> list[str]:
    frame = pd.DataFrame(level_rows)
    frame["fraction"] = frame["samples"] / total_samples
    order = [level for level in LEVEL_ORDER if level in set(frame["level"])]
    figure, axis = plt.subplots(figsize=(9, 4.5))
    sns.barplot(
        data=frame,
        x="level",
        y="fraction",
        order=order,
        hue="level",
        palette=COLORS,
        legend=False,
        ax=axis,
    )
    for patch, row in zip(axis.patches, frame.set_index("level").loc[order].to_dict("records")):
        axis.text(
            patch.get_x() + patch.get_width() / 2,
            patch.get_height() + 0.015,
            f'{int(row["samples"]):,}',
            ha="center",
            va="bottom",
            fontsize=8,
        )
    axis.set_ylim(0, 1.08)
    axis.yaxis.set_major_formatter(PercentFormatter(1.0))
    axis.set_xlabel("")
    axis.set_ylabel("Muestras que soportan la condición")
    axis.set_title("Cobertura por nivel de abstracción", loc="left")
    figure.tight_layout()
    return _save_figure(figure, output, "levels")


def _plot_heatmap(output: Path, cwe_rows: list[dict[str, Any]]) -> list[str]:
    matrix = pd.DataFrame(
        {
            level: {
                f'CWE-{row["target_cwe"]}': (
                    int(row["samples"])
                    if level in set(str(row["levels"]).split(" | "))
                    else None
                )
                for row in cwe_rows
            }
            for level in LEVEL_ORDER
        }
    )
    figure, axis = plt.subplots(figsize=(8.5, max(5.0, 0.38 * len(matrix) + 1.8)))
    axis.set_facecolor("#edf0ee")
    sns.heatmap(
        matrix,
        mask=matrix.isna(),
        cmap="crest",
        annot=True,
        fmt=".0f",
        linewidths=0.6,
        linecolor="white",
        cbar_kws={"label": "Muestras"},
        ax=axis,
    )
    axis.set_xlabel("Nivel disponible")
    axis.set_ylabel("CWE objetivo")
    axis.set_title("Matriz CWE × nivel disponible", loc="left")
    figure.tight_layout()
    return _save_figure(figure, output, "cwe_level_matrix")


def _plot_prompt_lengths(
    output: Path,
    prompt_lengths: dict[str, list[int]],
) -> list[str]:
    order = [level for level in LEVEL_ORDER if prompt_lengths.get(level)]
    statistics = []
    for level in order:
        values = prompt_lengths[level]
        statistics.append(
            {
                "label": level,
                "whislo": min(values),
                "q1": _quantile(values, 0.25),
                "med": _quantile(values, 0.5),
                "q3": _quantile(values, 0.75),
                "whishi": max(values),
                "fliers": [],
            }
        )
    figure, axis = plt.subplots(figsize=(9.5, max(3.4, 0.55 * len(order) + 1.5)))
    artists = axis.bxp(
        statistics,
        orientation="horizontal",
        patch_artist=True,
        showfliers=False,
    )
    for box, level in zip(artists["boxes"], order):
        box.set_facecolor(COLORS[level])
        box.set_alpha(0.8)
    axis.invert_yaxis()
    axis.set_xlabel("Caracteres por prompt")
    axis.set_ylabel("")
    axis.set_title("Longitud de prompt por nivel", loc="left")
    figure.tight_layout()
    return _save_figure(figure, output, "prompt_lengths")


def generate_distribution_figures(
    output: Path,
    *,
    total_samples: int,
    functional_samples: int,
    excluded_without_tests: int,
    cwe_rows: list[dict[str, Any]],
    level_rows: list[dict[str, Any]],
    pattern_rows: list[dict[str, Any]],
    prompt_lengths: dict[str, list[int]],
) -> list[str]:
    """Write all dataset-analysis figures through Seaborn/Matplotlib."""

    _plot_theme()
    for legacy in (
        "index.html",
        *(f"{stem}.svg" for stem in DISTRIBUTION_FIGURE_STEMS),
    ):
        legacy_path = output / legacy
        if legacy_path.exists():
            legacy_path.unlink()
    filenames = []
    filenames.extend(
        _plot_coverage(
            output,
            total_samples,
            functional_samples,
            excluded_without_tests,
        )
    )
    filenames.extend(
        _plot_horizontal_bars(
            output,
            "samples_by_cwe",
            "Muestras por CWE objetivo",
            ((f"CWE-{row['target_cwe']}", int(row["samples"])) for row in cwe_rows),
            color="#327a67",
        )
    )
    filenames.extend(_plot_levels(output, level_rows, functional_samples))
    filenames.extend(_plot_heatmap(output, cwe_rows))
    filenames.extend(
        _plot_horizontal_bars(
            output,
            "condition_patterns",
            "Patrones de condiciones por muestra",
            ((str(row["pattern"]), int(row["samples"])) for row in pattern_rows),
            color="#315c89",
        )
    )
    filenames.extend(_plot_prompt_lengths(output, prompt_lengths))
    return filenames


def build_distribution_report(
    dataset: str | Path,
    output_directory: str | Path,
    *,
    n: int = 30,
    include_cwe_description: bool = False,
) -> dict[str, Any]:
    """Compute distributions and write CSV, JSON, PNG and PDF artifacts."""

    if n < 1:
        raise ValueError("n debe ser al menos 1")
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    samples, coverage = load_samples(dataset)
    (
        selection_level_rows,
        selection_cwe_rows,
        selection_summary,
    ) = dataset_selection_distributions(dataset)

    by_cwe: Counter[int] = Counter()
    by_level: Counter[str] = Counter()
    patterns: Counter[tuple[str, ...]] = Counter()
    prompt_lengths: dict[str, list[int]] = defaultdict(list)
    cwe_levels: dict[int, tuple[str, ...]] = {}
    conditions_total = 0

    for sample in samples:
        conditions = build_prompt_conditions(
            sample,
            include_cwe_description=include_cwe_description,
        )
        levels = tuple(condition.level for condition in conditions)
        previous = cwe_levels.setdefault(sample.target_cwe, levels)
        if previous != levels:
            raise RuntimeError(
                f"CWE-{sample.target_cwe} tiene líneas canónicas inconsistentes"
            )
        by_cwe[sample.target_cwe] += 1
        by_level.update(levels)
        patterns[levels] += 1
        conditions_total += len(conditions)
        for condition in conditions:
            prompt_lengths[condition.level].append(len(condition.prompt))

    cwe_rows: list[dict[str, Any]] = []
    for cwe_id in sorted(by_cwe):
        levels = cwe_levels[cwe_id]
        sample_count = by_cwe[cwe_id]
        cwe_rows.append(
            {
                "target_cwe": cwe_id,
                "samples": sample_count,
                "levels": " | ".join(levels),
                "conditions_per_sample": len(levels),
                "prompt_conditions": sample_count * len(levels),
                "projected_generations": sample_count * len(levels) * n,
            }
        )

    level_rows = [
        {
            "level": level,
            "samples": by_level[level],
            "sample_percentage": round(100 * by_level[level] / len(samples), 3),
            "projected_generations": by_level[level] * n,
        }
        for level in LEVEL_ORDER
        if by_level[level]
    ]
    pattern_rows = [
        {
            "pattern": " → ".join(pattern),
            "conditions_per_sample": len(pattern),
            "samples": count,
            "sample_percentage": round(100 * count / len(samples), 3),
            "projected_generations": count * len(pattern) * n,
        }
        for pattern, count in sorted(
            patterns.items(), key=lambda item: (-item[1], item[0])
        )
    ]
    length_rows: list[dict[str, Any]] = []
    for level in LEVEL_ORDER:
        values = prompt_lengths.get(level, [])
        if not values:
            continue
        length_rows.append(
            {
                "level": level,
                "prompts": len(values),
                "min_characters": min(values),
                "q1_characters": round(_quantile(values, 0.25), 2),
                "median_characters": round(_quantile(values, 0.5), 2),
                "mean_characters": round(mean(values), 2),
                "q3_characters": round(_quantile(values, 0.75), 2),
                "max_characters": max(values),
            }
        )

    summary = {
        "dataset": str(Path(dataset).resolve()),
        "total_samples": coverage.total_samples,
        "functional_samples": len(samples),
        "excluded_without_tests": coverage.excluded_without_tests,
        "target_cwes": len(by_cwe),
        "prompt_conditions": conditions_total,
        "n": n,
        "projected_generations": conditions_total * n,
        "include_cwe_description": include_cwe_description,
        "selection_composition": selection_summary,
    }

    _write_csv(output / "samples_by_cwe.csv", cwe_rows)
    _write_csv(output / "levels.csv", level_rows)
    _write_csv(output / "condition_patterns.csv", pattern_rows)
    _write_csv(output / "prompt_lengths.csv", length_rows)
    _write_csv(
        output / "selection_by_target_abstraction.csv",
        selection_level_rows,
    )
    _write_csv(output / "selection_by_target_cwe.csv", selection_cwe_rows)

    figures = generate_distribution_figures(
        output,
        total_samples=coverage.total_samples,
        functional_samples=len(samples),
        excluded_without_tests=coverage.excluded_without_tests,
        cwe_rows=cwe_rows,
        level_rows=level_rows,
        pattern_rows=pattern_rows,
        prompt_lengths=prompt_lengths,
    )
    summary.update(
        {
            "figure_backend": "seaborn + matplotlib",
            "figures": figures,
        }
    )
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {**summary, "output_directory": str(output.resolve())}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("analysis/data-distribution"),
    )
    parser.add_argument("--n", type=int, default=30, help="Generaciones por condición")
    parser.add_argument("--include-cwe-description", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        summary = build_distribution_report(
            args.dataset,
            args.output_dir,
            n=args.n,
            include_cwe_description=args.include_cwe_description,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        raise SystemExit(f"error: {exc}") from exc
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
