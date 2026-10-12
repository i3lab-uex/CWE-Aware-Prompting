"""Run Bandit and extract the CWEs found in Python tasks."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import subprocess
import sys
from typing import Any, Sequence, TypedDict

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/bandit.log",
    filemode="a",
    format="%(filename)s - %(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CWEResult(TypedDict):
    """A CWE associated with the Python file that defines a task."""
    task_id: str
    cwe_id: int


class BanditError(RuntimeError):
    """Raised when Bandit cannot produce a valid report."""


def _run_bandit(directory: Path) -> dict[str, Any]:
    """Run Bandit on the given directory and return its JSON report."""
    command = [
        sys.executable,
        "-m",
        "bandit",
        "-r",
        str(directory),
        "-f",
        "json",
        "-q",
        "--exit-zero",
    ]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        logger.error("Bandit no se encontró en el entorno de Python actual.")
        raise BanditError(
            "No se encontró Bandit. Instálalo con `uv sync`."
        ) from exc

    if completed.returncode != 0:
        detail = completed.stderr.strip()
        message = f"Bandit terminó con el código {completed.returncode}"
        if detail:
            message = f"{message}: {detail}"
        logger.error(message)
        raise BanditError(message)

    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        logger.error("Bandit no devolvió un JSON válido")
        raise BanditError("Bandit no devolvió un JSON válido") from exc

    if not isinstance(report, dict) or not isinstance(report.get("results"), list):
        logger.error("El informe de Bandit no contiene una lista `results`")
        raise BanditError("El informe de Bandit no contiene una lista `results`")

    return report


def find_cwes(directory: str | Path) -> list[CWEResult]:
    """Return the unique ``(task_id, cwe_id)`` pairs reported by Bandit.

    ``task_id`` is the source file's basename without its ``.py`` extension.
    Results are sorted first by task identifier and then by CWE identifier.
    """

    target = Path(directory)
    if not target.exists():
        raise FileNotFoundError(f"El directorio no existe: {target}")
    if not target.is_dir():
        raise NotADirectoryError(f"La ruta no es un directorio: {target}")

    report = _run_bandit(target)
    unique_cwes: set[tuple[str, int]] = set()

    for finding in report["results"]:
        if not isinstance(finding, dict):
            continue

        filename = finding.get("filename")
        issue_cwe = finding.get("issue_cwe")
        if not isinstance(filename, str) or not isinstance(issue_cwe, dict):
            continue

        cwe_id = issue_cwe.get("id")
        if not isinstance(cwe_id, int) or isinstance(cwe_id, bool):
            continue

        unique_cwes.add((Path(filename).stem, cwe_id))

    return [
        {"task_id": task_id, "cwe_id": cwe_id}
        for task_id, cwe_id in sorted(unique_cwes)
    ]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ejecuta Bandit y devuelve los CWEs encontrados como JSON."
    )
    parser.add_argument("directory", help="Directorio que se analizará recursivamente")
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = _build_parser().parse_args(argv)

    try:
        results = find_cwes(args.directory)
    except (FileNotFoundError, NotADirectoryError, BanditError) as exc:
        raise Exception(f"Error al analizar {args.directory}: {exc}") from exc

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
