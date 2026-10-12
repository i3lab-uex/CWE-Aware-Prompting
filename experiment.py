"""CLI for CWE abstraction prompting experiments and result exploration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from cwe_experiment.dataset import DEFAULT_DATASET_PATH
from cwe_experiment.generation import REASONING_SETTINGS
from cwe_experiment.pipeline import RunConfig, run_experiment


def _csv_ints(values: list[str] | None) -> tuple[int, ...]:
    return tuple(int(item) for value in values or [] for item in value.split(",") if item)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="Genera, prueba y analiza el experimento")
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--base-url", required=True)
    run.add_argument("--model", required=True)
    run.add_argument("--n", type=int, required=True)
    run.add_argument("--api", choices=("chat-completions", "responses"), default="chat-completions")
    run.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    run.add_argument("--cwe", action="append", help="ID o lista separada por comas")
    run.add_argument("--sample-id", action="append", default=[])
    run.add_argument("--limit", type=int)
    run.add_argument("--concurrency", type=int, default=10)
    run.add_argument("--batch-size", type=int, default=100)
    run.add_argument("--temperature", type=float)
    run.add_argument(
        "--reasoning",
        "--reasoning-effort",
        dest="reasoning_effort",
        choices=tuple(sorted(REASONING_SETTINGS)),
        help=(
            "Esfuerzo de razonamiento enviado sin modificar al endpoint: "
            "on/off o none/minimal/low/medium/high/xhigh"
        ),
    )
    run.add_argument(
        "--max-tokens",
        type=int,
        help="Límite opcional de tokens de salida; si se omite, no se envía a la API",
    )
    run.add_argument("--retries", type=int, default=2)
    run.add_argument("--timeout", type=float, default=120.0)
    run.add_argument("--test-timeout", type=float, default=5.0)
    run.add_argument("--include-cwe-description", action="store_true")
    run.add_argument("--codeql", default="codeql")
    run.add_argument("--skip-tests", action="store_true")
    run.add_argument("--skip-bandit", action="store_true")
    run.add_argument("--skip-codeql", action="store_true")

    view = subparsers.add_parser("view", help="Sirve el viewer local")
    view.add_argument("--results", type=Path, required=True)
    view.add_argument("--host", default="127.0.0.1")
    view.add_argument("--port", type=int, default=8000)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "view":
        from cwe_experiment.viewer import serve

        serve(args.results, host=args.host, port=args.port)
        return 0
    if args.output.suffix.lower() != ".parquet":
        raise SystemExit("--output debe terminar en .parquet")
    config = RunConfig(
        output=args.output,
        base_url=args.base_url,
        model=args.model,
        n=args.n,
        api=args.api,
        dataset=args.dataset,
        cwes=_csv_ints(args.cwe),
        sample_ids=tuple(args.sample_id),
        limit=args.limit,
        concurrency=args.concurrency,
        batch_size=args.batch_size,
        temperature=args.temperature,
        reasoning_effort=args.reasoning_effort,
        max_tokens=args.max_tokens,
        retries=args.retries,
        timeout=args.timeout,
        test_timeout=args.test_timeout,
        include_cwe_description=args.include_cwe_description,
        codeql=args.codeql,
        skip_tests=args.skip_tests,
        skip_bandit=args.skip_bandit,
        skip_codeql=args.skip_codeql,
    )
    print(json.dumps(run_experiment(config), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
