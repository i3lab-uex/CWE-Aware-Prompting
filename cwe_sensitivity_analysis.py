"""CWE heterogeneity and CWE-502 sensitivity analysis for the Class contrast."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

import statistical_analysis as sa


OUTCOME_NAMES = (
    "overall_test_success",
    "safety_test_success",
    "target_cwe_present",
)
OUTCOME_BY_NAME = {outcome.name: outcome for outcome in sa.OUTCOMES}
OUTCOME_LABELS = {
    "overall_test_success": "Éxito conjunto de capacidad y seguridad",
    "safety_test_success": "Éxito de seguridad entre generaciones funcionales",
    "target_cwe_present": "Presencia de la CWE objetivo entre generaciones funcionales",
}
OUTPUT_DIR = Path("analysis/ReSAISE_sensitivity_CWE")


def holm(rows: list[dict[str, object]]) -> None:
    estimable = [
        (index, float(row["p_value"]))
        for index, row in enumerate(rows)
        if row.get("estimable") and math.isfinite(float(row["p_value"]))
    ]
    estimable.sort(key=lambda item: item[1])
    running = 0.0
    planned = len(OUTCOME_NAMES)
    for rank, (index, p_value) in enumerate(estimable):
        running = max(running, min(1.0, (planned - rank) * p_value))
        rows[index]["p_holm_3"] = running
    for row in rows:
        row.setdefault("p_holm_3", None)


def exact_glmm_without_502(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    filtered = [row for row in rows if int(row["target_cwe"]) != 502]
    for outcome_index, outcome_name in enumerate(OUTCOME_NAMES):
        outcome = OUTCOME_BY_NAME[outcome_name]
        selected, _ = sa.matched_rows(
            filtered,
            outcome,
            "Class",
            generic="Generic",
        )
        generic_events = sum(
            outcome.value(row)
            for row in selected
            if str(row["cwe_level"]) == "Generic"
        )
        class_events = sum(
            outcome.value(row)
            for row in selected
            if str(row["cwe_level"]) == "Class"
        )
        base = {
            "analysis": "task-random-intercept GLMM; CWE-502 excluded",
            "outcome": outcome_name,
            "tasks": len({str(row["task_id"]) for row in selected}),
            "generic_n": sum(
                str(row["cwe_level"]) == "Generic" for row in selected
            ),
            "class_n": sum(
                str(row["cwe_level"]) == "Class" for row in selected
            ),
            "generic_events": int(generic_events),
            "class_events": int(class_events),
        }
        if generic_events == 0 or class_events == 0:
            results.append(
                {
                    **base,
                    "estimable": False,
                    "reason": "complete separation (zero events in one arm)",
                    "rr": None,
                    "ci_low": None,
                    "ci_high": None,
                    "p_value": None,
                }
            )
            continue
        fit, warnings = sa.fit_mixed_glm(
            selected,
            outcome,
            "Class",
            generic="Generic",
            family="binomial",
            quadrature_points=15,
        )
        summary = sa.summarize_fit(
            fit,
            selected,
            outcome,
            "Class",
            generic="Generic",
            ci_draws=5000,
            seed=20260724 + outcome_index,
        )[0]
        results.append(
            {
                **base,
                "estimable": True,
                "rr": summary["relative_effect"],
                "ci_low": summary["relative_ci_low"],
                "ci_high": summary["relative_ci_high"],
                "p_value": summary["p_value"],
                "coefficient": summary["coefficient"],
                "coefficient_se": summary["coefficient_se"],
                "random_intercept_sd": fit.sigma,
                "warnings": warnings,
            }
        )
    holm(results)
    return results


def cwe_fixed_modified_poisson(
    rows: list[dict[str, object]],
    *,
    exclude_502: bool,
) -> list[dict[str, object]]:
    source = (
        [row for row in rows if int(row["target_cwe"]) != 502]
        if exclude_502
        else rows
    )
    results: list[dict[str, object]] = []
    for outcome_name in OUTCOME_NAMES:
        outcome = OUTCOME_BY_NAME[outcome_name]
        selected, _ = sa.matched_rows(
            source,
            outcome,
            "Class",
            generic="Generic",
        )
        y_all = np.asarray(
            [outcome.value(row) for row in selected],
            dtype=float,
        )
        generic_events = int(
            sum(
                value
                for value, row in zip(y_all, selected)
                if str(row["cwe_level"]) == "Generic"
            )
        )
        class_events = int(
            sum(
                value
                for value, row in zip(y_all, selected)
                if str(row["cwe_level"]) == "Class"
            )
        )
        base = {
            "analysis": (
                "CWE fixed effects + task-clustered modified Poisson"
                + ("; CWE-502 excluded" if exclude_502 else "")
            ),
            "outcome": outcome_name,
            "tasks": len({str(row["task_id"]) for row in selected}),
            "generic_n": sum(
                str(row["cwe_level"]) == "Generic" for row in selected
            ),
            "class_n": sum(
                str(row["cwe_level"]) == "Class" for row in selected
            ),
            "generic_events": generic_events,
            "class_events": class_events,
        }
        if generic_events == 0 or class_events == 0:
            results.append(
                {
                    **base,
                    "estimable": False,
                    "reason": "complete separation (zero events in one arm)",
                    "rr": None,
                    "ci_low": None,
                    "ci_high": None,
                    "p_value": None,
                    "cwes_informative": None,
                }
            )
            continue

        event_by_cwe: dict[int, float] = {}
        for value, row in zip(y_all, selected):
            cwe = int(row["target_cwe"])
            event_by_cwe[cwe] = event_by_cwe.get(cwe, 0.0) + value
        informative_cwes = sorted(
            cwe for cwe, events in event_by_cwe.items() if events > 0
        )
        informative = [
            (row, value)
            for row, value in zip(selected, y_all)
            if int(row["target_cwe"]) in informative_cwes
        ]
        reference_cwe = informative_cwes[0]
        cwe_columns = informative_cwes[1:]
        x = np.asarray(
            [
                [
                    1.0,
                    float(str(row["cwe_level"]) == "Class"),
                    *[
                        float(int(row["target_cwe"]) == cwe)
                        for cwe in cwe_columns
                    ],
                ]
                for row, _ in informative
            ],
            dtype=float,
        )
        y = np.asarray([value for _, value in informative], dtype=float)
        initial = np.zeros(x.shape[1], dtype=float)
        initial[0] = math.log(max(float(y.mean()), 1e-4))

        def objective(beta: np.ndarray) -> float:
            eta = np.clip(x @ beta, -30.0, 30.0)
            mu = np.exp(eta)
            return float(np.sum(mu - y * eta))

        def gradient(beta: np.ndarray) -> np.ndarray:
            eta = np.clip(x @ beta, -30.0, 30.0)
            return x.T @ (np.exp(eta) - y)

        fit = minimize(
            objective,
            initial,
            jac=gradient,
            method="L-BFGS-B",
            bounds=[(-20.0, 20.0)] * x.shape[1],
            options={"maxiter": 4000, "ftol": 1e-12, "gtol": 1e-8},
        )
        beta = np.asarray(fit.x, dtype=float)
        eta = np.clip(x @ beta, -30.0, 30.0)
        mu = np.exp(eta)
        bread = np.linalg.pinv(x.T @ (mu[:, None] * x), rcond=1e-10)
        cluster_scores: dict[str, np.ndarray] = {}
        for index, (row, _) in enumerate(informative):
            task = str(row["task_id"])
            score = x[index] * (y[index] - mu[index])
            cluster_scores[task] = cluster_scores.get(
                task,
                np.zeros(x.shape[1], dtype=float),
            ) + score
        meat = sum(
            np.outer(score, score) for score in cluster_scores.values()
        )
        clusters = len(cluster_scores)
        observations = len(informative)
        parameters = x.shape[1]
        correction = (
            clusters / max(clusters - 1, 1)
            * (observations - 1) / max(observations - parameters, 1)
        )
        covariance = bread @ meat @ bread * correction
        se = math.sqrt(max(float(covariance[1, 1]), 0.0))
        coefficient = float(beta[1])
        z_value = coefficient / se if se else math.inf
        p_value = float(2.0 * norm.sf(abs(z_value)))
        results.append(
            {
                **base,
                "estimable": bool(fit.success and abs(coefficient) < 19.9),
                "rr": math.exp(coefficient),
                "ci_low": math.exp(coefficient - 1.96 * se),
                "ci_high": math.exp(coefficient + 1.96 * se),
                "p_value": p_value,
                "coefficient": coefficient,
                "coefficient_se": se,
                "cwes_informative": len(informative_cwes),
                "reference_cwe": reference_cwe,
                "optimizer_success": bool(fit.success),
                "optimizer_message": str(fit.message),
            }
        )
    holm(results)
    return results


def primary_full(
    source_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    path = Path("analysis/ReSAISE/model_results.csv")
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    result = []
    for row in rows:
        if (
            row["treatment"] == "Class"
            and row["outcome"] in OUTCOME_NAMES
        ):
            outcome = OUTCOME_BY_NAME[row["outcome"]]
            selected, _ = sa.matched_rows(
                source_rows,
                outcome,
                "Class",
                generic="Generic",
            )
            result.append(
                {
                    "analysis": "primary task-random-intercept GLMM",
                    "outcome": row["outcome"],
                    "estimable": True,
                    "tasks": int(row["tasks"]),
                    "generic_n": int(row["generic_n"]),
                    "class_n": int(row["treatment_n"]),
                    "generic_events": int(
                        sum(
                            outcome.value(item)
                            for item in selected
                            if str(item["cwe_level"]) == "Generic"
                        )
                    ),
                    "class_events": int(
                        sum(
                            outcome.value(item)
                            for item in selected
                            if str(item["cwe_level"]) == "Class"
                        )
                    ),
                    "rr": float(row["relative_effect"]),
                    "ci_low": float(row["relative_ci_low"]),
                    "ci_high": float(row["relative_ci_high"]),
                    "p_value": float(row["p_value"]),
                    "p_holm_original": float(row["p_holm"]),
                }
            )
    return result


def format_effect(row: dict[str, object]) -> str:
    if not row.get("estimable"):
        return "NE"
    return (
        f'{float(row["rr"]):.3f} '
        f'[{float(row["ci_low"]):.3f}, {float(row["ci_high"]):.3f}]'
    )


def format_p(row: dict[str, object], key: str) -> str:
    value = row.get(key)
    if value is None:
        return "—"
    return f"{float(value):.4g}"


def report_markdown(output: dict[str, list[dict[str, object]]]) -> str:
    sections = [
        ("GLMM principal, corpus completo", "primary_full", "p_holm_original"),
        (
            "Efectos fijos de CWE, corpus completo",
            "cwe_fixed_full",
            "p_holm_3",
        ),
        (
            "GLMM principal, excluyendo CWE-502",
            "primary_without_502",
            "p_holm_3",
        ),
        (
            "Efectos fijos de CWE, excluyendo CWE-502",
            "cwe_fixed_without_502",
            "p_holm_3",
        ),
    ]
    lines = [
        "# Sensibilidad del efecto de Class a la heterogeneidad entre CWE y a CWE-502",
        "",
        "## Alcance",
        "",
        "Este análisis evalúa los tres contrastes de `Class` que fueron "
        "significativos en el análisis principal: éxito conjunto, éxito de los "
        "tests de seguridad entre generaciones funcionales y presencia de la "
        "CWE objetivo entre generaciones funcionales.",
        "",
        "Procedencia: `experiments/ReSAISE/results.parquet`; política de "
        "analizadores: `any`. Las poblaciones elegibles son las mismas que en "
        "el análisis principal.",
        "",
        "Se emplean dos especificaciones complementarias:",
        "",
        "1. el GLMM binomial-logit original, con intercepto aleatorio por tarea, "
        "reestimado tras excluir todas las tareas CWE-502;",
        "2. un modelo de Poisson modificado con efectos fijos de CWE objetivo y "
        "errores sándwich agrupados por tarea, ajustado con y sin CWE-502. Este "
        "modelo estima RR directamente.",
        "",
        "La columna Holm de sensibilidad corrige únicamente estos tres outcomes. "
        "Es un análisis suplementario y no sustituye las familias de "
        "multiplicidad del análisis confirmatorio principal.",
        "",
    ]
    for title, key, p_key in sections:
        lines.extend(
            [
                f"## {title}",
                "",
                "| Outcome | RR [IC 95 %] | p | p ajustado | Eventos Generic | Eventos Class |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for row in output[key]:
            lines.append(
                f'| {OUTCOME_LABELS[str(row["outcome"])]} '
                f'| {format_effect(row)} '
                f'| {format_p(row, "p_value")} '
                f'| {format_p(row, p_key)} '
                f'| {row.get("generic_events", "—")} '
                f'| {row.get("class_events", "—")} |'
            )
        lines.append("")

    no_502 = {
        str(row["outcome"]): row
        for row in output["primary_without_502"]
    }
    fixed_full = {
        str(row["outcome"]): row
        for row in output["cwe_fixed_full"]
    }
    fixed_no_502 = {
        str(row["outcome"]): row
        for row in output["cwe_fixed_without_502"]
    }

    def survives(row: dict[str, object], *, favorable_below: bool) -> bool:
        if not row.get("estimable") or row.get("p_holm_3") is None:
            return False
        effect = float(row["rr"])
        favorable = effect < 1.0 if favorable_below else effect > 1.0
        return favorable and float(row["p_holm_3"]) < 0.05

    lines.extend(
        [
            "## Interpretación",
            "",
            (
                "- Con efectos fijos explícitos de CWE objetivo, la ventaja en "
                f"éxito conjunto {'sobrevive' if survives(fixed_full['overall_test_success'], favorable_below=False) else 'no sobrevive'} "
                "a la corrección de sensibilidad para tres outcomes."
            ),
            (
                "- Con efectos fijos explícitos de CWE objetivo, la ventaja "
                f"condicional en seguridad {'sobrevive' if survives(fixed_full['safety_test_success'], favorable_below=False) else 'no sobrevive'} "
                "a la corrección de sensibilidad para tres outcomes."
            ),
            (
                "- Con efectos fijos explícitos de CWE objetivo, la reducción "
                f"de presencia de la CWE objetivo {'sobrevive' if survives(fixed_full['target_cwe_present'], favorable_below=True) else 'no sobrevive'} "
                "a la corrección de sensibilidad para tres outcomes cuando "
                "CWE-502 permanece en el corpus."
            ),
            (
                "- Tras excluir CWE-502, el GLMM original indica que la ventaja "
                f"en éxito conjunto {'se mantiene' if survives(no_502['overall_test_success'], favorable_below=False) else 'deja de estar respaldada'}."
            ),
            (
                "- Tras excluir CWE-502, el GLMM original indica que la ventaja "
                f"condicional en seguridad {'se mantiene' if survives(no_502['safety_test_success'], favorable_below=False) else 'deja de estar respaldada'}."
            ),
            (
                "- Tras excluir CWE-502, el contraste de presencia de la CWE "
                f"objetivo {'es estimable' if no_502['target_cwe_present'].get('estimable') else 'no es estimable'}; "
                f"los datos restantes contienen {no_502['target_cwe_present'].get('generic_events', '—')} "
                "evento Generic y "
                f"{no_502['target_cwe_present'].get('class_events', '—')} eventos Class."
            ),
            (
                "- El modelo con efectos fijos de CWE y sin CWE-502 conduce a "
                "la misma conclusión para la CWE objetivo: "
                f"{'respaldada' if survives(fixed_no_502['target_cwe_present'], favorable_below=True) else 'no respaldada'}."
            ),
            "",
            "Estos resultados deben tratarse como análisis de sensibilidad, no "
            "como nuevos tests confirmatorios. En particular, un brazo con cero "
            "eventos tras excluir CWE-502 produce separación y no permite "
            "establecer una reducción general de la CWE objetivo.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(output: dict[str, list[dict[str, object]]]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "sensitivity_results.json").write_text(
        json.dumps(output, indent=2, allow_nan=False),
        encoding="utf-8",
    )
    all_rows = [
        row
        for key in (
            "primary_full",
            "cwe_fixed_full",
            "primary_without_502",
            "cwe_fixed_without_502",
        )
        for row in output[key]
    ]
    fieldnames = sorted({key for row in all_rows for key in row})
    with (OUTPUT_DIR / "sensitivity_results.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    (OUTPUT_DIR / "informe_sensibilidad_CWE.md").write_text(
        report_markdown(output),
        encoding="utf-8",
    )


def main() -> int:
    raw = sa.load_results(Path("experiments/ReSAISE"))
    rows = sa.flatten_rows(raw, analyzer_policy="any")
    output = {
        "primary_full": primary_full(rows),
        "cwe_fixed_full": cwe_fixed_modified_poisson(
            rows,
            exclude_502=False,
        ),
        "primary_without_502": exact_glmm_without_502(rows),
        "cwe_fixed_without_502": cwe_fixed_modified_poisson(
            rows,
            exclude_502=True,
        ),
    }
    write_outputs(output)
    print(json.dumps(output, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
