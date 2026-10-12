"""Load the functional subset of the insecure-coding benchmark."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


DEFAULT_DATASET_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "insecure_coding-00000-of-00001.parquet"
)
TASK_FIELDS = (
    "description",
    "function_name",
    "arguments",
    "context",
    "return",
    "raise",
)


@dataclass(frozen=True)
class Sample:
    """The only benchmark fields allowed to reach generation/evaluation."""

    task_id: str
    target_cwe: int
    description: str
    function_name: str
    arguments: str
    context: str
    returns: str
    raises: str
    setup: str
    testcases: str
    install_requires: tuple[str, ...]

    @property
    def task(self) -> dict[str, str]:
        return {
            "description": self.description,
            "function_name": self.function_name,
            "arguments": self.arguments,
            "context": self.context,
            "return": self.returns,
            "raise": self.raises,
        }


@dataclass(frozen=True)
class Coverage:
    total_samples: int
    selected_samples: int
    excluded_without_tests: int
    selected_cwes: tuple[int, ...]


def _normalise_dependencies(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if hasattr(value, "tolist"):
        value = value.tolist()
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    return tuple(str(item) for item in value if str(item).strip())


def _read_rows(path: Path) -> list[dict[str, Any]]:
    """Read through PyArrow, with pandas as a compatibility fallback."""

    try:
        import pyarrow.parquet as pq

        return pq.read_table(path).to_pylist()
    except ImportError:
        try:
            import pandas as pd
        except ImportError as exc:  # pragma: no cover - installation failure
            raise RuntimeError("Se requiere pyarrow para leer el dataset") from exc
        return pd.read_parquet(path).to_dict(orient="records")


def _field(row: dict[str, Any], dotted_name: str) -> Any:
    """Read either Arrow nested structs or pandas' flattened column names."""

    if dotted_name in row:
        return row[dotted_name]
    value: Any = row
    for part in dotted_name.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def load_samples(
    path: str | Path = DEFAULT_DATASET_PATH,
    *,
    cwes: Iterable[int] | None = None,
    sample_ids: Iterable[str] | None = None,
    limit: int | None = None,
) -> tuple[list[Sample], Coverage]:
    """Return samples with non-empty functional tests and coverage metadata."""

    if limit is not None and limit < 1:
        raise ValueError("limit debe ser al menos 1")
    dataset_path = Path(path)
    rows = _read_rows(dataset_path)
    allowed_cwes = set(cwes) if cwes is not None else None
    allowed_ids = set(sample_ids) if sample_ids is not None else None
    functional_rows = [
        row for row in rows if str(_field(row, "unittest.testcases") or "").strip()
    ]
    all_cwes = tuple(sorted({int(row["CWE_ID"]) for row in functional_rows}))
    selected: list[Sample] = []
    for row in functional_rows:
        cwe_id = int(row["CWE_ID"])
        task_id = str(row["id"])
        if allowed_cwes is not None and cwe_id not in allowed_cwes:
            continue
        if allowed_ids is not None and task_id not in allowed_ids:
            continue
        selected.append(
            Sample(
                task_id=task_id,
                target_cwe=cwe_id,
                description=str(_field(row, "task_description.description") or ""),
                function_name=str(_field(row, "task_description.function_name") or ""),
                arguments=str(_field(row, "task_description.arguments") or ""),
                context=str(_field(row, "task_description.context") or ""),
                returns=str(_field(row, "task_description.return") or ""),
                raises=str(_field(row, "task_description.raise") or ""),
                setup=str(_field(row, "unittest.setup") or ""),
                testcases=str(_field(row, "unittest.testcases") or ""),
                install_requires=_normalise_dependencies(row.get("install_requires")),
            )
        )
        if limit is not None and len(selected) >= limit:
            break

    coverage = Coverage(
        total_samples=len(rows),
        selected_samples=len(functional_rows),
        excluded_without_tests=len(rows) - len(functional_rows),
        selected_cwes=all_cwes,
    )
    return selected, coverage
