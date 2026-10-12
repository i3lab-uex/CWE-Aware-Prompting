"""Select a matched checkpoint sample, then run tests, Bandit, and CodeQL."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import tempfile
from typing import Any, Sequence

from cwe_experiment.dataset import load_samples
from cwe_experiment.evaluation import EphemeralEnvironment
from cwe_experiment.pipeline import (
    RunConfig,
    _apply_analyzers,
    _evaluate_rows,
    _materialise,
    _persist_failure_artifacts,
    _sample_map,
)
from cwe_experiment.progress import ConsoleProgress
from cwe_experiment.storage import FragmentStore
from statistical_analysis import LEVEL_ORDER, load_results


def select_matched_rows(
    rows: Sequence[dict[str, Any]],
    *,
    sample_size: int,
    repetitions: int,
    seed: int,
    generic: str = "Generic",
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return disjoint task pairs: Generic plus one CWE condition per task."""

    rows_per_task = 2 * repetitions
    if sample_size % rows_per_task:
        raise ValueError(
            f"sample-size debe ser múltiplo de {rows_per_task} "
            f"para conservar {repetitions} repeticiones en cada par"
        )
    task_target = sample_size // rows_per_task
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(
            (str(row["task_id"]), str(row["cwe_level"])), []
        ).append(row)
    complete: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for key, values in grouped.items():
        by_index = {
            int(row["generation_index"]): row
            for row in values
        }
        if len(by_index) >= repetitions:
            complete[key] = [
                by_index[index] for index in sorted(by_index)[:repetitions]
            ]
    treatments = [
        level
        for level in LEVEL_ORDER
        if level != generic
        and any(condition == level for _, condition in complete)
    ]
    if not treatments:
        raise RuntimeError("No hay condiciones CWE completas en los checkpoints")

    candidates = {
        treatment: sorted(
            task
            for task, condition in complete
            if condition == treatment and (task, generic) in complete
        )
        for treatment in treatments
    }
    randomizer = random.Random(seed)
    for values in candidates.values():
        randomizer.shuffle(values)

    base, extra = divmod(task_target, len(treatments))
    quotas = {
        treatment: base + int(index < extra)
        for index, treatment in enumerate(treatments)
    }
    selected: dict[str, list[str]] = {treatment: [] for treatment in treatments}
    used_tasks: set[str] = set()
    # Preserve rare abstraction levels before drawing from common conditions.
    for treatment in sorted(treatments, key=lambda item: len(candidates[item])):
        available = [
            task for task in candidates[treatment] if task not in used_tasks
        ]
        chosen = available[: quotas[treatment]]
        selected[treatment].extend(chosen)
        used_tasks.update(chosen)

    deficit = task_target - len(used_tasks)
    while deficit:
        progress = False
        for treatment in treatments:
            available = next(
                (
                    task
                    for task in candidates[treatment]
                    if task not in used_tasks
                ),
                None,
            )
            if available is None:
                continue
            selected[treatment].append(available)
            used_tasks.add(available)
            deficit -= 1
            progress = True
            if not deficit:
                break
        if not progress:
            raise RuntimeError(
                f"Sólo hay {len(used_tasks)} tareas emparejadas disjuntas; "
                f"se necesitan {task_target}"
            )

    sampled_rows: list[dict[str, Any]] = []
    selection: list[dict[str, Any]] = []
    for treatment in treatments:
        for task in selected[treatment]:
            generic_rows = complete[(task, generic)]
            treatment_rows = complete[(task, treatment)]
            sampled_rows.extend(generic_rows)
            sampled_rows.extend(treatment_rows)
            selection.append(
                {
                    "task_id": task,
                    "treatment": treatment,
                    "generic": generic,
                    "repetitions_per_condition": repetitions,
                    "rows": len(generic_rows) + len(treatment_rows),
                }
            )
    if len(sampled_rows) != sample_size:
        raise AssertionError(
            f"la muestra contiene {len(sampled_rows)} filas, no {sample_size}"
        )
    return sampled_rows, selection


def reset_downstream_results(rows: Sequence[dict[str, Any]]) -> None:
    """Force tests and analyzers to run even when source checkpoints are merged."""

    for row in rows:
        available = row.get("generation_status") == "ok"
        downstream_status = "pending" if available else "skipped_generation_error"
        row.update(
            {
                "syntax_valid": None,
                "evaluation_status": downstream_status,
                "evaluation_error": None,
                "test_total": 0,
                "test_passed": 0,
                "capability_total": 0,
                "capability_passed": 0,
                "safety_total": 0,
                "safety_passed": 0,
                "all_tests_pass": False,
                "test_timeout": False,
                "import_error": False,
                "syntax_error": False,
                "runtime_error": False,
                "test_results": [],
                "bandit_status": downstream_status,
                "bandit_error": None,
                "bandit_findings": [],
                "bandit_version": "",
                "codeql_status": downstream_status,
                "codeql_error": None,
                "codeql_findings": [],
                "codeql_version": "",
                "target_cwe_detected": False,
                "prompt_cwe_detected": False,
                "any_cwe_detected": False,
                "generated_file": None,
            }
        )


def _run_config(config: dict[str, Any], output: Path) -> RunConfig:
    return RunConfig(
        output=output,
        base_url=str(config["base_url"]),
        model=str(config["model"]),
        n=int(config["n"]),
        api=str(config.get("api", "chat-completions")),
        dataset=Path(config["dataset"]),
        cwes=tuple(int(value) for value in config.get("cwes") or ()),
        sample_ids=(),
        limit=None,
        concurrency=int(config.get("concurrency", 1)),
        batch_size=int(config.get("batch_size", 100)),
        temperature=config.get("temperature"),
        reasoning_effort=config.get("reasoning_effort"),
        max_tokens=config.get("max_tokens"),
        retries=int(config.get("retries", 2)),
        timeout=float(config.get("timeout", 120.0)),
        test_timeout=float(config.get("test_timeout", 5.0)),
        include_cwe_description=bool(config.get("include_cwe_description", False)),
        codeql=str(config.get("codeql", "codeql")),
        skip_tests=False,
        skip_bandit=False,
        skip_codeql=False,
    )


def run_sample_evaluation(args: argparse.Namespace) -> dict[str, Any]:
    manifest_path = args.run / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_config = dict(manifest["config"])
    repetitions = int(source_config["n"])
    sampled_rows, selection = select_matched_rows(
        load_results(args.run / "checkpoints"),
        sample_size=args.sample_size,
        repetitions=repetitions,
        seed=args.seed,
        generic=args.generic,
    )
    reset_downstream_results(sampled_rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "results.parquet"
    config = _run_config(source_config, output)
    store_config = {
        **config.manifest(),
        "source_run_id": manifest["run_id"],
        "sample_size": args.sample_size,
        "sample_seed": args.seed,
        "sample_strategy": "disjoint matched tasks, Generic plus one CWE condition",
    }
    store = FragmentStore(output, config=store_config)
    if not store.rows():
        for offset in range(0, len(sampled_rows), config.batch_size):
            store.write_batch(
                "generation",
                offset // config.batch_size,
                sampled_rows[offset : offset + config.batch_size],
            )
    selection_path = args.output_dir / "selection.json"
    selection_path.write_text(
        json.dumps(
            {
                "source_run_id": manifest["run_id"],
                "sample_size": args.sample_size,
                "seed": args.seed,
                "strategy": "disjoint matched tasks, Generic plus one CWE condition",
                "by_treatment": {
                    treatment: sum(item["treatment"] == treatment for item in selection)
                    for treatment in sorted({item["treatment"] for item in selection})
                },
                "tasks": selection,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    samples, _ = load_samples(
        config.dataset,
        sample_ids={item["task_id"] for item in selection},
    )
    if len(samples) != len(selection):
        raise RuntimeError(
            f"Se recuperaron {len(samples)} muestras del dataset para "
            f"{len(selection)} tareas seleccionadas"
        )
    dependencies = {
        dependency for sample in samples for dependency in sample.install_requires
    }
    progress = ConsoleProgress()
    progress.message(
        "muestra",
        f"{len(selection)} tareas · {len(sampled_rows)} filas · seed={args.seed}",
    )
    try:
        with tempfile.TemporaryDirectory(prefix="cwe-sample-evaluation-") as temporary:
            environment = EphemeralEnvironment(Path(temporary))
            progress.message(
                "entorno",
                "preparando dependencias"
                + (
                    f" ({', '.join(sorted(dependencies))})"
                    if dependencies
                    else ""
                ),
            )
            environment.create(dependencies)
            rows = store.rows()
            paths = _materialise(environment, rows)
            _evaluate_rows(
                config,
                environment,
                rows,
                _sample_map(samples),
                store,
                progress,
            )
            rows = store.rows()
            _persist_failure_artifacts(environment, rows, store)
            paths = _materialise(environment, rows)
            _apply_analyzers(
                config,
                environment,
                rows,
                paths,
                store,
                progress,
            )
        store.compact()
        rows = store.rows()
        summary = {
            "source_run_id": manifest["run_id"],
            "sample_size": len(rows),
            "tasks": len(selection),
            "selection_by_treatment": {
                treatment: sum(item["treatment"] == treatment for item in selection)
                for treatment in sorted({item["treatment"] for item in selection})
            },
            "generation_failures": sum(
                row["generation_status"] != "ok" for row in rows
            ),
            "evaluation_complete": sum(
                row["evaluation_status"] == "complete" for row in rows
            ),
            "all_tests_pass": sum(row.get("all_tests_pass") is True for row in rows),
            "bandit_complete": sum(row["bandit_status"] == "complete" for row in rows),
            "codeql_complete": sum(row["codeql_status"] == "complete" for row in rows),
            "results": str(output),
            "selection": str(selection_path),
        }
        store.mark_complete(**summary)
        return summary
    except BaseException as error:
        store.mark_failed(error)
        raise


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sample-size", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260723)
    parser.add_argument("--generic", default="Generic")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    summary = run_sample_evaluation(args)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
