"""Nested Parquet fragments and atomic experiment compaction."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any, Iterable
from datetime import datetime, timezone
import uuid


ROW_KEY_FIELDS = ("task_id", "cwe_level", "generation_index")
OPERATIONAL_CONFIG_FIELDS = frozenset({"output", "concurrency"})


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _semantic_config(config: dict[str, Any]) -> dict[str, Any]:
    semantic = {
        key: value
        for key, value in config.items()
        if key not in OPERATIONAL_CONFIG_FIELDS
    }
    # This nullable field was introduced after the first checkpoint format.
    # Omitting its default keeps those experiments resumable.
    if semantic.get("reasoning_effort") is None:
        semantic.pop("reasoning_effort", None)
    return semantic


def _execution_record(
    config: dict[str, Any],
    *,
    started_at: str,
    resume_count: int,
) -> dict[str, Any]:
    return {
        "started_at": started_at,
        "resume_count": resume_count,
        "concurrency": config.get("concurrency"),
    }


def result_schema() -> Any:
    import pyarrow as pa

    test_result = pa.struct(
        [
            ("category", pa.string()),
            ("test_index", pa.int32()),
            ("passed", pa.bool_()),
            ("status", pa.string()),
            ("expected", pa.string()),
            ("actual", pa.string()),
            ("error", pa.string()),
            ("captured_output", pa.string()),
            ("duration_ms", pa.float64()),
        ]
    )
    finding = pa.struct(
        [
            ("source", pa.string()),
            ("suite", pa.string()),
            ("cwe", pa.int32()),
            ("rule", pa.string()),
            ("severity", pa.string()),
            ("confidence", pa.string()),
            ("message", pa.string()),
            ("line", pa.int32()),
            ("column", pa.int32()),
            ("end_line", pa.int32()),
            ("end_column", pa.int32()),
        ]
    )
    summary = pa.struct([("type", pa.string()), ("text", pa.string())])
    return pa.schema(
        [
            ("run_id", pa.string()),
            ("task_id", pa.string()),
            ("target_cwe", pa.int32()),
            ("cwe_level", pa.string()),
            ("prompt_cwe", pa.int32()),
            ("prompt_cwe_name", pa.string()),
            ("generation_index", pa.int32()),
            ("prompt", pa.string()),
            ("model", pa.string()),
            ("api", pa.string()),
            ("base_url", pa.string()),
            ("temperature", pa.float64()),
            ("reasoning_effort", pa.string()),
            ("max_tokens", pa.int32()),
            ("timeout_seconds", pa.float64()),
            ("max_retries", pa.int32()),
            ("openai_version", pa.string()),
            ("bandit_version", pa.string()),
            ("codeql_version", pa.string()),
            ("codeql_suites", pa.list_(pa.string())),
            ("raw_response", pa.string()),
            ("reasoning_native", pa.string()),
            ("reasoning_extracted", pa.string()),
            ("reasoning_summaries", pa.list_(summary)),
            ("code", pa.string()),
            ("latency_ms", pa.float64()),
            ("input_tokens", pa.int64()),
            ("output_tokens", pa.int64()),
            ("total_tokens", pa.int64()),
            ("reasoning_tokens", pa.int64()),
            ("generation_status", pa.string()),
            ("generation_error", pa.string()),
            ("generation_attempts", pa.int32()),
            ("syntax_valid", pa.bool_()),
            ("evaluation_status", pa.string()),
            ("evaluation_error", pa.string()),
            ("test_total", pa.int32()),
            ("test_passed", pa.int32()),
            ("capability_total", pa.int32()),
            ("capability_passed", pa.int32()),
            ("safety_total", pa.int32()),
            ("safety_passed", pa.int32()),
            ("all_tests_pass", pa.bool_()),
            ("test_timeout", pa.bool_()),
            ("import_error", pa.bool_()),
            ("syntax_error", pa.bool_()),
            ("runtime_error", pa.bool_()),
            ("test_results", pa.list_(test_result)),
            ("bandit_status", pa.string()),
            ("bandit_error", pa.string()),
            ("bandit_findings", pa.list_(finding)),
            ("codeql_status", pa.string()),
            ("codeql_error", pa.string()),
            ("codeql_findings", pa.list_(finding)),
            ("target_cwe_detected", pa.bool_()),
            ("prompt_cwe_detected", pa.bool_()),
            ("any_cwe_detected", pa.bool_()),
            ("generated_file", pa.string()),
        ]
    )


def row_key(row: dict[str, Any]) -> tuple[str, str, int]:
    return (str(row["task_id"]), str(row["cwe_level"]), int(row["generation_index"]))


def _normalise_row(row: dict[str, Any]) -> dict[str, Any]:
    return {name: row.get(name) for name in result_schema().names}


def write_parquet(path: str | Path, rows: Iterable[dict[str, Any]]) -> None:
    import pyarrow as pa
    import pyarrow.parquet as pq

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    data = [_normalise_row(row) for row in rows]
    table = pa.Table.from_pylist(data, schema=result_schema())
    pq.write_table(table, output, compression="zstd")


def read_parquet(path: str | Path) -> list[dict[str, Any]]:
    import pyarrow.parquet as pq
    import pyarrow as pa

    target = Path(path)
    if not target.exists():
        return []
    # Rebuild through Python rows so older checkpoints gain newly introduced
    # nullable fields (including nested ones) during schema evolution.
    return pa.Table.from_pylist(
        pq.read_table(target).to_pylist(), schema=result_schema()
    ).to_pylist()


class FragmentStore:
    """Deterministic stage/batch fragments with last-stage-wins merging."""

    def __init__(self, output: str | Path, *, config: dict[str, Any]) -> None:
        self.output = Path(output)
        self.run_directory = self.output.parent
        self.run_directory.mkdir(parents=True, exist_ok=True)
        legacy_directory = self.output.parent / f".{self.output.name}.fragments"
        legacy_manifest = legacy_directory / "manifest.json"
        self.directory = (
            legacy_directory
            if legacy_manifest.exists() and not (self.run_directory / "manifest.json").exists()
            else self.run_directory / "checkpoints"
        )
        self.directory.mkdir(parents=True, exist_ok=True)
        self.logs_directory = self.run_directory / "logs"
        self.reports_directory = self.run_directory / "reports"
        self.failures_directory = self.run_directory / "failures"
        for path in (self.logs_directory, self.reports_directory, self.failures_directory):
            path.mkdir(parents=True, exist_ok=True)
        self.log_path = self.logs_directory / "run.log"
        self.events_path = self.logs_directory / "events.jsonl"
        self.manifest_path = (
            legacy_manifest if self.directory == legacy_directory else self.run_directory / "manifest.json"
        )
        semantic_config = _semantic_config(config)
        serialised = json.dumps(semantic_config, sort_keys=True, separators=(",", ":"))
        self.fingerprint = hashlib.sha256(serialised.encode()).hexdigest()
        operational_changes: dict[str, dict[str, Any]] = {}
        if self.manifest_path.exists():
            manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            existing_config = manifest.get("config") or {}
            existing_semantic = _semantic_config(existing_config)
            existing_fingerprint = hashlib.sha256(
                json.dumps(existing_semantic, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
            if existing_fingerprint != self.fingerprint:
                raise RuntimeError(
                    "Los fragmentos existentes pertenecen a otra configuración; "
                    f"mueva o elimine {self.directory}"
                )
            self.run_id = str(manifest["run_id"])
            resumed_at = _utc_now()
            resume_count = int(manifest.get("resume_count", 0)) + 1
            operational_changes = {
                key: {
                    "previous": existing_config.get(key),
                    "current": config.get(key),
                }
                for key in OPERATIONAL_CONFIG_FIELDS
                if key != "output" and existing_config.get(key) != config.get(key)
            }
            execution_history = manifest.get("execution_history")
            if not isinstance(execution_history, list):
                execution_history = []
            if not execution_history:
                execution_history.append(
                    _execution_record(
                        existing_config,
                        started_at=str(manifest.get("started_at", resumed_at)),
                        resume_count=0,
                    )
                )
            execution_history.append(
                _execution_record(
                    config,
                    started_at=resumed_at,
                    resume_count=resume_count,
                )
            )
            manifest.update(
                config_hash=self.fingerprint,
                config=config,
                status="running",
                updated_at=resumed_at,
                last_resumed_at=resumed_at,
                resume_count=resume_count,
                execution_history=execution_history,
            )
            self._manifest = manifest
            _atomic_json(self.manifest_path, manifest)
        else:
            started_at = _utc_now()
            self.run_id = (
                datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                + "-"
                + uuid.uuid4().hex[:8]
            )
            self._manifest = {
                "schema_version": 1,
                "run_id": self.run_id,
                "config_hash": self.fingerprint,
                "status": "running",
                "started_at": started_at,
                "updated_at": started_at,
                "finished_at": None,
                "resume_count": 0,
                "config": config,
                "execution_history": [
                    _execution_record(config, started_at=started_at, resume_count=0)
                ],
                "storage": {
                    "results": str(self.output),
                    "checkpoints": str(self.directory),
                    "logs": str(self.logs_directory),
                    "reports": str(self.reports_directory),
                    "failures": str(self.failures_directory),
                },
            }
            _atomic_json(self.manifest_path, self._manifest)
        self.log(f"run {self.run_id} started (config {self.fingerprint[:12]})")
        if operational_changes:
            self.log(f"operational configuration changed: {operational_changes}")
        self.append_event(
            "run_started",
            resume_count=self._manifest.get("resume_count", 0),
            concurrency=config.get("concurrency"),
            operational_changes=operational_changes,
        )

    @property
    def manifest(self) -> dict[str, Any]:
        return dict(self._manifest)

    def update_manifest(self, **values: Any) -> None:
        self._manifest.update(values, updated_at=_utc_now())
        _atomic_json(self.manifest_path, self._manifest)

    def log(self, message: str, *, level: str = "INFO") -> None:
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"{_utc_now()} {level} {message}\n")

    def append_event(self, event: str, **values: Any) -> None:
        record = {"timestamp": _utc_now(), "event": event, **values}
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    def mark_complete(self, **summary: Any) -> None:
        finished_at = _utc_now()
        duration = (
            datetime.fromisoformat(finished_at)
            - datetime.fromisoformat(str(self._manifest["started_at"]))
        ).total_seconds()
        self.update_manifest(
            status="complete",
            finished_at=finished_at,
            duration_seconds=duration,
            summary=summary,
        )
        self.append_event("run_completed", **summary)
        self.log("run completed")

    def mark_failed(self, error: BaseException) -> None:
        message = f"{type(error).__name__}: {error}"
        finished_at = _utc_now()
        duration = (
            datetime.fromisoformat(finished_at)
            - datetime.fromisoformat(str(self._manifest["started_at"]))
        ).total_seconds()
        self.update_manifest(
            status="failed",
            finished_at=finished_at,
            duration_seconds=duration,
            error=message,
        )
        self.append_event("run_failed", error=message)
        self.log(message, level="ERROR")

    def fragment_path(self, key: tuple[str, str, int]) -> Path:
        raw = "\0".join(map(str, key))
        digest = hashlib.sha256(raw.encode()).hexdigest()[:16]
        slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{key[0]}-{key[1]}-{key[2]}")
        return self.directory / f"{slug[:80]}-{digest}.parquet"

    def write(self, row: dict[str, Any]) -> Path:
        """Write one keyed update (primarily useful for small callers/tests)."""

        path = self.fragment_path(row_key(row))
        temporary = path.with_suffix(".tmp.parquet")
        write_parquet(temporary, [row])
        os.replace(temporary, path)
        return path

    def write_batch(self, stage: str, batch_index: int, rows: Iterable[dict[str, Any]]) -> Path:
        """Atomically replace one deterministic pipeline batch fragment."""

        if stage not in {"generation", "evaluation", "analysis"}:
            raise ValueError(f"Etapa de fragmento inválida: {stage}")
        path = self.directory / f"{stage}-{batch_index:08d}.parquet"
        temporary = path.with_suffix(".tmp.parquet")
        write_parquet(temporary, rows)
        os.replace(temporary, path)
        return path

    def rows(self) -> list[dict[str, Any]]:
        priority = {"generation": 0, "evaluation": 1, "analysis": 2}

        def ordering(path: Path) -> tuple[int, str]:
            stage = path.name.split("-", 1)[0]
            # Per-key update fragments intentionally win over pipeline stages.
            return priority.get(stage, 3), path.name

        merged: dict[tuple[str, str, int], dict[str, Any]] = {}
        for fragment in sorted(self.directory.glob("*.parquet"), key=ordering):
            for row in read_parquet(fragment):
                merged[row_key(row)] = row
        return sorted(merged.values(), key=row_key)

    def by_key(self) -> dict[tuple[str, str, int], dict[str, Any]]:
        return {row_key(row): row for row in self.rows()}

    def compact(self) -> Path:
        rows = self.rows()
        temporary = self.output.with_suffix(self.output.suffix + ".tmp")
        write_parquet(temporary, rows)
        os.replace(temporary, self.output)
        return self.output
