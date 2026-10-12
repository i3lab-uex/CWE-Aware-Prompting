"""Batch Bandit and CodeQL execution plus CWE mapping."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any
from urllib.parse import unquote, urlparse

from .evaluation import EphemeralEnvironment


CWE_TAG = re.compile(r"(?:external/)?cwe/cwe[-_](\d+)", re.IGNORECASE)
CODEQL_SUITES = {
    "stable": "codeql/python-queries:codeql-suites/python-security-and-quality.qls",
    "experimental": "codeql/python-queries:experimental/Security",
}


@dataclass
class AnalyzerReport:
    status: str
    version: str = ""
    findings_by_file: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    error: str | None = None


def _location(
    location: dict[str, Any], source_root: Path
) -> tuple[str, dict[str, int | None]]:
    physical = location.get("physicalLocation", location)
    artifact = physical.get("artifactLocation", {})
    uri = unquote(str(artifact.get("uri", "")))
    parsed = urlparse(uri)
    raw_path = parsed.path if parsed.scheme == "file" else uri
    path = Path(raw_path)
    if not path.is_absolute():
        path = source_root / path
    region = physical.get("region", {})
    return str(path.resolve()), {
        "line": region.get("startLine"),
        "column": region.get("startColumn"),
        "end_line": region.get("endLine"),
        "end_column": region.get("endColumn"),
    }


def parse_bandit_report(report: dict[str, Any], source_root: Path) -> dict[str, list[dict[str, Any]]]:
    mapped: dict[str, list[dict[str, Any]]] = {}
    for result in report.get("results", []):
        path = Path(str(result.get("filename", "")))
        if not path.is_absolute():
            path = source_root / path
        filename = str(path.resolve())
        cwe = (result.get("issue_cwe") or {}).get("id")
        finding = {
            "source": "bandit",
            "suite": "bandit",
            "cwe": int(cwe) if isinstance(cwe, int) else None,
            "rule": str(result.get("test_id", "")),
            "severity": str(result.get("issue_severity", "")).lower(),
            "confidence": str(result.get("issue_confidence", "")).lower(),
            "message": str(result.get("issue_text", "")),
            "line": result.get("line_number"),
            "column": result.get("col_offset"),
            "end_line": result.get("end_line_number"),
            "end_column": result.get("end_col_offset"),
        }
        mapped.setdefault(filename, []).append(finding)
    return mapped


def run_bandit(
    environment: EphemeralEnvironment, *, report_directory: Path | None = None
) -> AnalyzerReport:
    version_call = subprocess.run(
        environment.command(["-m", "bandit", "--version"]),
        cwd=environment.root,
        env=environment.env,
        capture_output=True,
        text=True,
        check=False,
    )
    version_match = re.search(r"\bbandit\s+([0-9][^\s]*)", version_call.stdout, re.IGNORECASE)
    version = version_match.group(1) if version_match else ""
    command = environment.command(
        ["-m", "bandit", "-r", str(environment.generations), "-f", "json", "-q", "--exit-zero"]
    )
    try:
        completed = subprocess.run(
            command,
            cwd=environment.root,
            env=environment.env,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        return AnalyzerReport(status="error", error=f"{type(exc).__name__}: {exc}")
    if completed.returncode:
        return AnalyzerReport(status="error", error=completed.stderr.strip() or f"exit {completed.returncode}")
    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return AnalyzerReport(status="error", error=f"JSON inválido: {exc}")
    if report_directory is not None:
        report_directory.mkdir(parents=True, exist_ok=True)
        destination = report_directory / "bandit.json"
        temporary = destination.with_suffix(".tmp.json")
        temporary.write_text(completed.stdout, encoding="utf-8")
        temporary.replace(destination)
    return AnalyzerReport(
        status="complete",
        version=version,
        findings_by_file=parse_bandit_report(report, environment.generations),
    )


def parse_sarif_report(
    report: dict[str, Any], source_root: Path, suite: str
) -> dict[str, list[dict[str, Any]]]:
    mapped: dict[str, list[dict[str, Any]]] = {}
    for run in report.get("runs", []):
        rules = {
            str(rule.get("id")): rule
            for rule in (run.get("tool", {}).get("driver", {}).get("rules", []) or [])
        }
        for result in run.get("results", []) or []:
            rule_id = str(result.get("ruleId", ""))
            rule = rules.get(rule_id, {})
            tags = [
                *rule.get("properties", {}).get("tags", []),
                *result.get("properties", {}).get("tags", []),
            ]
            cwes = sorted({int(match.group(1)) for tag in tags if (match := CWE_TAG.search(str(tag)))})
            message = result.get("message", {}).get("text", "")
            severity = str(result.get("level") or result.get("properties", {}).get("problem.severity", ""))
            for raw_location in result.get("locations", []) or [{}]:
                filename, region = _location(raw_location, source_root)
                for cwe in cwes or [None]:
                    mapped.setdefault(filename, []).append(
                        {
                            "source": "codeql",
                            "suite": suite,
                            "cwe": cwe,
                            "rule": rule_id,
                            "severity": severity.lower(),
                            "confidence": "",
                            "message": str(message),
                            **region,
                        }
                    )
    return mapped


def _merge_findings(
    target: dict[str, list[dict[str, Any]]], source: dict[str, list[dict[str, Any]]]
) -> None:
    for filename, findings in source.items():
        target.setdefault(filename, []).extend(findings)


def run_codeql(
    environment: EphemeralEnvironment,
    *,
    executable: str = "codeql",
    suites: dict[str, str] = CODEQL_SUITES,
    report_directory: Path | None = None,
) -> AnalyzerReport:
    resolved = shutil.which(executable) if "/" not in executable else executable
    if not resolved:
        return AnalyzerReport(status="unavailable", error=f"No se encontró CodeQL: {executable}")
    version_call = subprocess.run(
        [resolved, "version", "--format=json"],
        env=environment.env,
        capture_output=True,
        text=True,
        check=False,
    )
    version = ""
    if version_call.returncode == 0:
        try:
            version = str(json.loads(version_call.stdout).get("version", ""))
        except json.JSONDecodeError:
            version = version_call.stdout.strip()
    database = environment.analysis / "codeql-db"
    create = subprocess.run(
        [
            resolved,
            "database",
            "create",
            str(database),
            "--language=python",
            f"--source-root={environment.generations}",
            "--overwrite",
        ],
        cwd=environment.root,
        env=environment.env,
        capture_output=True,
        text=True,
        check=False,
    )
    if create.returncode:
        return AnalyzerReport(
            status="error",
            version=version,
            error=create.stderr.strip() or f"database create exit {create.returncode}",
        )
    mapped: dict[str, list[dict[str, Any]]] = {}
    errors: list[str] = []
    for label, suite in suites.items():
        sarif = environment.analysis / f"codeql-{label}.sarif"
        analyze = subprocess.run(
            [
                resolved,
                "database",
                "analyze",
                str(database),
                suite,
                "--format=sarif-latest",
                f"--output={sarif}",
                "--threads=0",
                "--download",
            ],
            cwd=environment.root,
            env=environment.env,
            capture_output=True,
            text=True,
            check=False,
        )
        if analyze.returncode:
            errors.append(f"{label}: {analyze.stderr.strip() or analyze.returncode}")
            continue
        try:
            report = json.loads(sarif.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{label}: SARIF inválido ({exc})")
            continue
        if report_directory is not None:
            report_directory.mkdir(parents=True, exist_ok=True)
            destination = report_directory / f"codeql-{label}.sarif"
            temporary = destination.with_suffix(".tmp.sarif")
            shutil.copy2(sarif, temporary)
            temporary.replace(destination)
        _merge_findings(mapped, parse_sarif_report(report, environment.generations, label))
    status = "complete" if not errors else ("partial" if mapped else "error")
    return AnalyzerReport(status=status, version=version, findings_by_file=mapped, error="; ".join(errors) or None)


def detections(
    target_cwe: int,
    prompt_cwe: int | None,
    bandit_findings: list[dict[str, Any]],
    codeql_findings: list[dict[str, Any]],
) -> tuple[bool, bool, bool]:
    found = {item.get("cwe") for item in [*bandit_findings, *codeql_findings] if item.get("cwe") is not None}
    return target_cwe in found, prompt_cwe is not None and prompt_cwe in found, bool(found)
