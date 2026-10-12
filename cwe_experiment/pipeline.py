"""End-to-end generation, evaluation, analysis, and compaction."""

from __future__ import annotations

import ast
import asyncio
from dataclasses import asdict, dataclass
import importlib.metadata
import json
from pathlib import Path
import platform
import re
import tempfile
from typing import Any

from .analyzers import CODEQL_SUITES, detections, run_bandit, run_codeql
from .dataset import DEFAULT_DATASET_PATH, Sample, load_samples
from .evaluation import EphemeralEnvironment, TestExecutor
from .generation import GenerationInput, OpenAIGenerator
from .prompts import PromptCondition, build_prompt_conditions
from .progress import ConsoleProgress
from .storage import FragmentStore, row_key


@dataclass(frozen=True)
class RunConfig:
    output: Path
    base_url: str
    model: str
    n: int
    api: str = "chat-completions"
    dataset: Path = DEFAULT_DATASET_PATH
    cwes: tuple[int, ...] = ()
    sample_ids: tuple[str, ...] = ()
    limit: int | None = None
    concurrency: int = 10
    batch_size: int = 100
    temperature: float | None = None
    reasoning_effort: str | None = None
    max_tokens: int | None = None
    retries: int = 2
    timeout: float = 120.0
    test_timeout: float = 5.0
    include_cwe_description: bool = False
    codeql: str = "codeql"
    skip_tests: bool = False
    skip_bandit: bool = False
    skip_codeql: bool = False

    def manifest(self) -> dict[str, Any]:
        data = asdict(self)
        data["output"] = str(self.output.resolve())
        data["dataset"] = str(self.dataset.resolve())
        return data


def _version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return ""


def _base_row(
    config: RunConfig,
    run_id: str,
    sample: Sample,
    condition: PromptCondition,
    index: int,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "task_id": sample.task_id,
        "target_cwe": sample.target_cwe,
        "cwe_level": condition.level,
        "prompt_cwe": condition.prompt_cwe,
        "prompt_cwe_name": condition.prompt_cwe_name,
        "generation_index": index,
        "prompt": condition.prompt,
        "model": config.model,
        "api": config.api,
        "base_url": config.base_url,
        "temperature": config.temperature,
        "reasoning_effort": config.reasoning_effort,
        "max_tokens": config.max_tokens,
        "timeout_seconds": config.timeout,
        "max_retries": config.retries,
        "openai_version": _version("openai"),
        "bandit_version": "",
        "codeql_version": "",
        "codeql_suites": list(CODEQL_SUITES),
        "raw_response": "",
        "reasoning_native": "",
        "reasoning_extracted": "",
        "reasoning_summaries": [],
        "code": "",
        "latency_ms": 0.0,
        "input_tokens": None,
        "output_tokens": None,
        "total_tokens": None,
        "reasoning_tokens": None,
        "generation_status": "pending",
        "generation_error": None,
        "generation_attempts": 0,
        "syntax_valid": None,
        "evaluation_status": "pending",
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
        "bandit_status": "pending",
        "bandit_error": None,
        "bandit_findings": [],
        "codeql_status": "pending",
        "codeql_error": None,
        "codeql_findings": [],
        "target_cwe_detected": False,
        "prompt_cwe_detected": False,
        "any_cwe_detected": False,
        "generated_file": None,
    }


def _safe_filename(row: dict[str, Any]) -> str:
    raw = f"{row['task_id']}__{row['cwe_level']}__{row['generation_index']:04d}.py"
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", raw)


async def _generate_missing(
    config: RunConfig,
    jobs: list[tuple[Sample, PromptCondition, int]],
    store: FragmentStore,
    client: Any | None,
    progress: ConsoleProgress,
) -> None:
    existing = store.by_key()
    completed_total = sum(
        (sample.task_id, condition.level, index) in existing
        for sample, condition, index in jobs
    )
    progress.update(
        "generation",
        completed_total,
        len(jobs),
        "reanudado" if completed_total else "iniciando",
        force=True,
    )
    if completed_total == len(jobs):
        return
    generator = OpenAIGenerator(
        model=config.model,
        base_url=config.base_url,
        api=config.api,  # type: ignore[arg-type]
        concurrency=config.concurrency,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        retries=config.retries,
        timeout=config.timeout,
        reasoning_effort=config.reasoning_effort,
        client=client,
    )
    for offset in range(0, len(jobs), config.batch_size):
        full_batch = jobs[offset : offset + config.batch_size]
        batch = [
            job
            for job in full_batch
            if (job[0].task_id, job[1].level, job[2]) not in existing
        ]
        if not batch:
            continue
        requests = [
            GenerationInput(
                prompt=condition.prompt,
                generation_index=index,
                metadata={
                    "task_id": sample.task_id,
                    "cwe_level": condition.level,
                },
            )
            for sample, condition, index in batch
        ]
        def generated(_: int, __: int, result: Any) -> None:
            nonlocal completed_total
            completed_total += 1
            progress.update(
                "generation",
                completed_total,
                len(jobs),
                f"último={result.status}",
            )

        results = await generator.generate_many(requests, progress_callback=generated)
        updated: dict[tuple[str, str, int], dict[str, Any]] = {
            key: existing[key]
            for sample, condition, index in full_batch
            if (key := (sample.task_id, condition.level, index)) in existing
        }
        for (sample, condition, index), result in zip(batch, results):
            row = _base_row(config, store.run_id, sample, condition, index)
            row.update(
                raw_response=result.raw_response,
                reasoning_native=result.reasoning_native,
                reasoning_extracted=result.reasoning_extracted,
                reasoning_summaries=result.reasoning_summaries,
                code=result.code,
                latency_ms=result.latency_ms,
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
                total_tokens=result.total_tokens,
                reasoning_tokens=result.reasoning_tokens,
                generation_status=result.status,
                generation_error=result.error,
                generation_attempts=result.attempts,
            )
            if result.status == "ok":
                try:
                    ast.parse(result.code)
                    row["syntax_valid"] = True
                except SyntaxError:
                    row["syntax_valid"] = False
                    row["syntax_error"] = True
            else:
                row["evaluation_status"] = "skipped_generation_error"
                row["bandit_status"] = "skipped_generation_error"
                row["codeql_status"] = "skipped_generation_error"
            updated[row_key(row)] = row
        batch_index = offset // config.batch_size
        store.write_batch("generation", batch_index, updated.values())
        store.append_event(
            "generation_batch_completed",
            batch_index=batch_index,
            requested=len(batch),
            successful=sum(result.status == "ok" for result in results),
            failed=sum(result.status != "ok" for result in results),
        )
        store.log(
            f"generation batch {batch_index} completed: "
            f"{sum(result.status == 'ok' for result in results)}/{len(results)} successful"
        )


def _sample_map(samples: list[Sample]) -> dict[str, Sample]:
    return {sample.task_id: sample for sample in samples}


def _materialise(environment: EphemeralEnvironment, rows: list[dict[str, Any]]) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for row in rows:
        if row["generation_status"] != "ok":
            continue
        filename = _safe_filename(row)
        path = environment.generations / filename
        path.write_text(str(row.get("code") or ""), encoding="utf-8")
        row["generated_file"] = filename
        paths[filename] = path.resolve()
    return paths


def _evaluate_rows(
    config: RunConfig,
    environment: EphemeralEnvironment,
    rows: list[dict[str, Any]],
    samples: dict[str, Sample],
    store: FragmentStore,
    progress: ConsoleProgress,
) -> None:
    executor = TestExecutor(environment, timeout=config.test_timeout)
    total = sum(row["generation_status"] == "ok" for row in rows)
    completed = sum(
        row["generation_status"] == "ok"
        and row["evaluation_status"] not in {"pending", None}
        for row in rows
    )
    progress.update("tests", completed, total, "iniciando", force=True)
    for offset in range(0, len(rows), config.batch_size):
        batch = rows[offset : offset + config.batch_size]
        changed = False
        for row in batch:
            if row["generation_status"] != "ok" or row["evaluation_status"] not in {"pending", None}:
                continue
            changed = True
            if config.skip_tests:
                row["evaluation_status"] = "skipped"
                completed += 1
                progress.update("tests", completed, total, "omitidos")
                continue
            key = f"{row['task_id']}__{row['cwe_level']}__{row['generation_index']:04d}"
            result = executor.evaluate(samples[row["task_id"]], row["code"], key)
            row.update(result.summary())
            completed += 1
            progress.update(
                "tests",
                completed,
                total,
                f"último={row['test_passed']}/{row['test_total']}",
            )
        if changed:
            batch_index = offset // config.batch_size
            store.write_batch("evaluation", batch_index, batch)
            evaluated = [
                row
                for row in batch
                if row["generation_status"] == "ok"
                and row["evaluation_status"] not in {"pending", None}
            ]
            store.append_event(
                "evaluation_batch_completed",
                batch_index=batch_index,
                evaluated=len(evaluated),
                all_tests_pass=sum(row.get("all_tests_pass") is True for row in evaluated),
            )
            store.log(f"evaluation batch {batch_index} completed: {len(evaluated)} rows")


def _apply_analyzers(
    config: RunConfig,
    environment: EphemeralEnvironment,
    rows: list[dict[str, Any]],
    paths: dict[str, Path],
    store: FragmentStore,
    progress: ConsoleProgress,
) -> None:
    analyzable = [row for row in rows if row["generation_status"] == "ok"]
    need_bandit = not config.skip_bandit and any(row["bandit_status"] == "pending" for row in analyzable)
    need_codeql = not config.skip_codeql and any(row["codeql_status"] == "pending" for row in analyzable)
    if need_bandit:
        progress.message("Bandit", f"analizando {len(analyzable):,} generaciones en un lote")
    elif config.skip_bandit:
        progress.message("Bandit", "omitido por configuración")
    bandit = (
        run_bandit(environment, report_directory=store.reports_directory)
        if need_bandit
        else None
    )
    if bandit is not None:
        store.append_event(
            "bandit_completed",
            status=bandit.status,
            version=bandit.version,
            findings=sum(len(items) for items in bandit.findings_by_file.values()),
            error=bandit.error,
        )
        store.log(f"Bandit finished with status {bandit.status}")
        progress.message(
            "Bandit",
            f"estado={bandit.status}, hallazgos="
            f"{sum(len(items) for items in bandit.findings_by_file.values()):,}",
        )
    if need_codeql:
        progress.message(
            "CodeQL",
            f"analizando {len(analyzable):,} generaciones con suites stable y experimental",
        )
    elif config.skip_codeql:
        progress.message("CodeQL", "omitido por configuración")
    codeql = (
        run_codeql(
            environment,
            executable=config.codeql,
            report_directory=store.reports_directory,
        )
        if need_codeql
        else None
    )
    if codeql is not None:
        store.append_event(
            "codeql_completed",
            status=codeql.status,
            version=codeql.version,
            findings=sum(len(items) for items in codeql.findings_by_file.values()),
            error=codeql.error,
        )
        store.log(f"CodeQL finished with status {codeql.status}")
        progress.message(
            "CodeQL",
            f"estado={codeql.status}, hallazgos="
            f"{sum(len(items) for items in codeql.findings_by_file.values()):,}",
        )
    for row in analyzable:
        filename = str(paths[row["generated_file"]])
        if config.skip_bandit and row["bandit_status"] == "pending":
            row["bandit_status"] = "skipped"
        elif bandit is not None:
            row["bandit_status"] = bandit.status
            row["bandit_error"] = bandit.error
            row["bandit_version"] = bandit.version
            row["bandit_findings"] = bandit.findings_by_file.get(filename, [])
        if config.skip_codeql and row["codeql_status"] == "pending":
            row["codeql_status"] = "skipped"
        elif codeql is not None:
            row["codeql_status"] = codeql.status
            row["codeql_error"] = codeql.error
            row["codeql_version"] = codeql.version
            row["codeql_findings"] = codeql.findings_by_file.get(filename, [])
        target, prompt, any_found = detections(
            row["target_cwe"],
            row["prompt_cwe"],
            row["bandit_findings"],
            row["codeql_findings"],
        )
        row["target_cwe_detected"] = target
        row["prompt_cwe_detected"] = prompt
        row["any_cwe_detected"] = any_found
    for offset in range(0, len(rows), config.batch_size):
        store.write_batch(
            "analysis", offset // config.batch_size, rows[offset : offset + config.batch_size]
        )


def _persist_failure_artifacts(
    environment: EphemeralEnvironment | None,
    rows: list[dict[str, Any]],
    store: FragmentStore,
) -> None:
    persisted = 0
    for row in rows:
        status = row.get("evaluation_status")
        key = f"{row['task_id']}__{row['cwe_level']}__{row['generation_index']:04d}"
        if row.get("generation_status") != "ok":
            destination = store.failures_directory / key
            destination.mkdir(parents=True, exist_ok=True)
            (destination / "generation-error.json").write_text(
                json.dumps(
                    {
                        "task_id": row["task_id"],
                        "target_cwe": row["target_cwe"],
                        "cwe_level": row["cwe_level"],
                        "prompt_cwe": row["prompt_cwe"],
                        "generation_index": row["generation_index"],
                        "generation_status": row["generation_status"],
                        "generation_error": row.get("generation_error"),
                        "generation_attempts": row.get("generation_attempts"),
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            persisted += 1
            continue
        if environment is None or status in {
            "pending",
            "skipped",
            "skipped_generation_error",
            None,
        }:
            continue
        if row.get("all_tests_pass") is True:
            continue
        destination = store.failures_directory / key
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "generated.py").write_text(str(row.get("code") or ""), encoding="utf-8")
        (destination / "result.json").write_text(
            json.dumps(
                {
                    "task_id": row["task_id"],
                    "target_cwe": row["target_cwe"],
                    "cwe_level": row["cwe_level"],
                    "prompt_cwe": row["prompt_cwe"],
                    "generation_index": row["generation_index"],
                    "evaluation_status": status,
                    "syntax_valid": row.get("syntax_valid"),
                    "test_results": row.get("test_results") or [],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        payload = environment.tests / key / "payload.json"
        if payload.is_file():
            (destination / "payload.json").write_bytes(payload.read_bytes())
        persisted += 1
    store.append_event("failure_artifacts_persisted", count=persisted)
    if persisted:
        store.log(f"persisted {persisted} failed generation artifacts", level="WARNING")


def run_experiment(
    config: RunConfig,
    *,
    client: Any | None = None,
    progress: ConsoleProgress | None = None,
) -> dict[str, Any]:
    progress = progress or ConsoleProgress()
    if config.n < 1:
        raise ValueError("n debe ser al menos 1")
    if config.batch_size < 1:
        raise ValueError("batch-size debe ser al menos 1")
    samples, coverage = load_samples(
        config.dataset,
        cwes=config.cwes or None,
        sample_ids=config.sample_ids or None,
        limit=config.limit,
    )
    if not samples:
        raise RuntimeError("Los filtros no seleccionaron ninguna muestra funcional")
    jobs = [
        (sample, condition, index)
        for sample in samples
        for condition in build_prompt_conditions(
            sample, include_cwe_description=config.include_cwe_description
        )
        for index in range(config.n)
    ]
    store = FragmentStore(config.output, config=config.manifest())
    coverage_manifest = {
        **asdict(coverage),
        "run_selected_samples": len(samples),
        "run_selected_cwes": sorted({sample.target_cwe for sample in samples}),
    }
    plan = {
        "conditions": len(jobs) // config.n,
        "generations": len(jobs),
        "n": config.n,
    }
    store.update_manifest(
        experiment_name=store.run_directory.name,
        coverage=coverage_manifest,
        plan=plan,
        tools={"python": platform.python_version(), "openai": _version("openai")},
    )
    store.append_event("experiment_planned", **plan, selected_samples=len(samples))
    reasoning = config.reasoning_effort or "predeterminado del modelo"
    progress.message("experimento", f"{store.run_directory} · run_id={store.run_id}")
    progress.message(
        "config",
        f"modelo={config.model} · API={config.api} · reasoning={reasoning} "
        f"· temperature={config.temperature} · N={config.n}",
    )
    progress.message(
        "plan",
        f"{len(samples):,} muestras · {plan['conditions']:,} condiciones "
        f"· {plan['generations']:,} generaciones",
    )
    try:
        asyncio.run(_generate_missing(config, jobs, store, client, progress))
        rows = store.rows()
        actionable = [row for row in rows if row["generation_status"] == "ok"]
        needs_environment = any(
            row["evaluation_status"] == "pending"
            or row["bandit_status"] == "pending"
            or row["codeql_status"] == "pending"
            for row in actionable
        )
        if needs_environment:
            dependencies = {
                dependency for sample in samples for dependency in sample.install_requires
            }
            store.append_event(
                "environment_preparation_started", dependencies=sorted(dependencies)
            )
            progress.message(
                "entorno",
                "preparando aislamiento temporal"
                + (f" · dependencias={','.join(sorted(dependencies))}" if dependencies else ""),
            )
            with tempfile.TemporaryDirectory(prefix="cwe-prompting-") as temporary:
                environment = EphemeralEnvironment(Path(temporary))
                environment.create(dependencies)
                store.append_event("environment_ready")
                progress.message("entorno", "listo")
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
                # Reload test updates before applying the two batch analyzers.
                paths = _materialise(environment, rows)
                _apply_analyzers(config, environment, rows, paths, store, progress)
        else:
            _persist_failure_artifacts(None, rows, store)
        progress.message("Parquet", "compactando checkpoints de forma atómica")
        output = store.compact()
        rows = store.rows()
        tools = {
            "python": platform.python_version(),
            "openai": _version("openai"),
            "bandit": next(
                (str(row["bandit_version"]) for row in rows if row.get("bandit_version")),
                "",
            ),
            "codeql": next(
                (str(row["codeql_version"]) for row in rows if row.get("codeql_version")),
                "",
            ),
        }
        summary = {
            "rows": len(rows),
            "valid_code": sum(row.get("syntax_valid") is True for row in rows),
            "all_tests_pass": sum(row.get("all_tests_pass") is True for row in rows),
            "generation_errors": sum(row.get("generation_status") != "ok" for row in rows),
            "rows_with_cwe_findings": sum(
                row.get("any_cwe_detected") is True for row in rows
            ),
            "output": str(output),
        }
        store.update_manifest(tools=tools)
        store.mark_complete(**summary)
        progress.message(
            "completado",
            f"{len(rows):,} filas · código válido={summary['valid_code']:,} "
            f"· tests superados={summary['all_tests_pass']:,} · {output}",
        )
        return {
            "run_id": store.run_id,
            "experiment_name": store.run_directory.name,
            "config_hash": store.fingerprint,
            "run_directory": str(store.run_directory),
            "output": str(config.output),
            "rows": len(rows),
            "conditions": plan["conditions"],
            "generations": plan["generations"],
            "coverage": asdict(coverage),
        }
    except BaseException as exc:
        store.mark_failed(exc)
        progress.message("error", f"{type(exc).__name__}: {exc}")
        raise
