"""Ephemeral environment and per-testcase sandbox execution."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import subprocess
from typing import Any, Iterable
import venv

from .dataset import Sample


ALLOWED_SAMPLE_DEPENDENCIES = {"numpy", "sympy", "pyyaml", "requests"}


@dataclass
class EvaluationResult:
    syntax_valid: bool
    status: str
    test_results: list[dict[str, Any]] = field(default_factory=list)
    timeout: bool = False
    import_error: bool = False
    syntax_error: bool = False
    runtime_error: bool = False
    error: str | None = None

    def summary(self) -> dict[str, Any]:
        result = self.test_results
        capability = [item for item in result if item["category"] == "capability"]
        safety = [item for item in result if item["category"] == "safety"]
        passed = sum(bool(item["passed"]) for item in result)
        return {
            "syntax_valid": self.syntax_valid,
            "evaluation_status": self.status,
            "evaluation_error": self.error,
            "test_total": len(result),
            "test_passed": passed,
            "capability_total": len(capability),
            "capability_passed": sum(bool(item["passed"]) for item in capability),
            "safety_total": len(safety),
            "safety_passed": sum(bool(item["passed"]) for item in safety),
            "all_tests_pass": bool(result) and passed == len(result),
            "test_timeout": self.timeout,
            "import_error": self.import_error,
            "syntax_error": self.syntax_error,
            "runtime_error": self.runtime_error,
            "test_results": result,
        }


class EphemeralEnvironment:
    """One redirected temporary environment for a complete run."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.home = self.root / "home"
        self.tmp = self.root / "tmp"
        self.cache = self.root / "cache"
        self.venv = self.root / "venv"
        self.generations = self.root / "generations"
        self.tests = self.root / "tests"
        self.analysis = self.root / "analysis"
        for path in (
            self.home,
            self.tmp,
            self.cache,
            self.generations,
            self.tests,
            self.analysis,
        ):
            path.mkdir(parents=True, exist_ok=True)
        self.python = self.venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        self.sandbox_profile: Path | None = None

    @property
    def env(self) -> dict[str, str]:
        env = os.environ.copy()
        env.update(
            HOME=str(self.home),
            TMPDIR=str(self.tmp),
            TMP=str(self.tmp),
            TEMP=str(self.tmp),
            XDG_CACHE_HOME=str(self.cache),
            PIP_CACHE_DIR=str(self.cache / "pip"),
            UV_CACHE_DIR=str(self.cache / "uv"),
            PYTHONNOUSERSITE="1",
            OPENBLAS_NUM_THREADS="1",
            OMP_NUM_THREADS="1",
            MKL_NUM_THREADS="1",
            NO_PROXY="*",
            no_proxy="*",
        )
        for key in (
            "DISPLAY",
            "HTTP_PROXY",
            "HTTPS_PROXY",
            "ALL_PROXY",
            "http_proxy",
            "https_proxy",
            "all_proxy",
        ):
            env.pop(key, None)
        return env

    def create(self, dependencies: Iterable[str]) -> None:
        dependencies = {item.lower() for item in dependencies}
        unsupported = dependencies - ALLOWED_SAMPLE_DEPENDENCIES
        if unsupported:
            raise RuntimeError(f"Dependencias de muestra no permitidas: {sorted(unsupported)}")
        venv.EnvBuilder(with_pip=True, clear=True).create(self.venv)
        packages = ["bandit", *sorted(dependencies)]
        completed = subprocess.run(
            [str(self.python), "-m", "pip", "install", "--disable-pip-version-check", *packages],
            env=self.env,
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode:
            raise RuntimeError(f"No se pudo preparar el venv: {completed.stderr.strip()}")
        if platform.system() == "Darwin":
            self._activate_macos_sandbox()

    def _activate_macos_sandbox(self) -> None:
        executable = shutil.which("sandbox-exec")
        if executable is None:
            raise RuntimeError("sandbox-exec no está disponible; ejecución cerrada por seguridad")
        escaped = str(self.root).replace('"', '\\"')
        profile = self.root / "sandbox.sb"
        profile.write_text(
            "(version 1)\n"
            "(allow default)\n"
            "(deny network*)\n"
            "(deny file-write*)\n"
            f'(allow file-write* (subpath "{escaped}"))\n',
            encoding="utf-8",
        )
        probe = subprocess.run(
            [executable, "-f", str(profile), "/usr/bin/true"],
            capture_output=True,
            text=True,
            check=False,
        )
        if probe.returncode:
            raise RuntimeError(f"No se pudo activar sandbox-exec: {probe.stderr.strip()}")
        self.sandbox_profile = profile

    def command(self, arguments: list[str]) -> list[str]:
        command = [str(self.python), *arguments]
        if self.sandbox_profile is not None:
            command = ["sandbox-exec", "-f", str(self.sandbox_profile), *command]
        return command


def _resource_limits(cpu_seconds: int, file_bytes: int, processes: int) -> Any:
    if os.name == "nt":
        return None

    def apply() -> None:
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds + 1))
        resource.setrlimit(resource.RLIMIT_FSIZE, (file_bytes, file_bytes))
        if hasattr(resource, "RLIMIT_NPROC"):
            resource.setrlimit(resource.RLIMIT_NPROC, (processes, processes))
        if hasattr(resource, "RLIMIT_NOFILE"):
            resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))

    return apply


class TestExecutor:
    __test__ = False

    def __init__(
        self,
        environment: EphemeralEnvironment,
        *,
        timeout: float = 5.0,
        cpu_seconds: int = 4,
        file_bytes: int = 1_048_576,
        processes: int = 1,
    ) -> None:
        self.environment = environment
        self.timeout = timeout
        self.preexec_fn = _resource_limits(cpu_seconds, file_bytes, processes)
        self.worker = Path(__file__).with_name("case_worker.py").resolve()

    def _invoke(self, payload: Path, cwd: Path, extra: list[str]) -> dict[str, Any]:
        cwd.mkdir(parents=True, exist_ok=True)
        command = self.environment.command(
            [str(self.worker), str(payload), "--root", str(self.environment.root), *extra]
        )
        try:
            completed = subprocess.run(
                command,
                cwd=cwd,
                env=self.environment.env,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
                preexec_fn=self.preexec_fn,
            )
        except subprocess.TimeoutExpired:
            return {"worker_error": "timeout", "error": f"timeout after {self.timeout}s"}
        if completed.returncode:
            return {
                "worker_error": "runtime_error",
                "error": completed.stderr.strip() or f"worker exit {completed.returncode}",
            }
        try:
            return json.loads(completed.stdout)
        except json.JSONDecodeError:
            return {"worker_error": "runtime_error", "error": "worker returned invalid JSON"}

    def evaluate(self, sample: Sample, code: str, key: str) -> EvaluationResult:
        try:
            ast.parse(code)
        except SyntaxError as exc:
            return EvaluationResult(
                syntax_valid=False,
                status="syntax_error",
                syntax_error=True,
                error=f"{type(exc).__name__}: {exc}",
            )
        base = self.environment.tests / key
        base.mkdir(parents=True, exist_ok=True)
        payload = base / "payload.json"
        payload.write_text(
            json.dumps(
                {
                    "setup": sample.setup,
                    "testcases": sample.testcases,
                    "code": code,
                    "function_name": sample.function_name,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        discovery = self._invoke(payload, base / "discovery", ["--list"])
        if "worker_error" in discovery:
            kind = discovery["worker_error"]
            return EvaluationResult(
                syntax_valid=True,
                status=kind,
                timeout=kind == "timeout",
                import_error=kind == "import_error",
                syntax_error=kind == "syntax_error",
                runtime_error=kind == "runtime_error",
                error=discovery.get("error"),
            )
        results: list[dict[str, Any]] = []
        flags = {"timeout": False, "import_error": False, "syntax_error": False, "runtime_error": False}
        for category in ("capability", "safety"):
            for index in range(int(discovery["counts"].get(category, 0))):
                response = self._invoke(
                    payload,
                    base / f"{category}-{index:04d}",
                    ["--category", category, "--index", str(index)],
                )
                worker_error = response.get("worker_error")
                if worker_error:
                    if worker_error in flags:
                        flags[worker_error] = True
                    response = {
                        "passed": False,
                        "status": worker_error,
                        "expected": "",
                        "actual": "",
                        "error": response.get("error"),
                        "duration_ms": 0.0,
                    }
                results.append({"category": category, "test_index": index, **response})
        passed = sum(bool(item["passed"]) for item in results)
        return EvaluationResult(
            syntax_valid=True,
            status="complete" if not any(flags.values()) else "error",
            test_results=results,
            **flags,
        )
