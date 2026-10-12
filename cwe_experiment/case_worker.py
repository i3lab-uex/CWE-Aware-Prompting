"""Minimal subprocess worker for one isolated benchmark testcase."""

from __future__ import annotations

import argparse
import ast
import builtins
import contextlib
import io
import json
import os
from pathlib import Path
import shlex
import socket
import subprocess
import sys
import time
import types
from typing import Any


def _inside(path: str | bytes | os.PathLike[str] | os.PathLike[bytes], root: Path) -> bool:
    try:
        candidate = Path(os.fsdecode(path)).resolve()
        candidate.relative_to(root)
        return True
    except (OSError, TypeError, ValueError):
        return False


def _install_guards(root: Path) -> None:
    """Deny network/processes and writes outside the run directory."""

    def audit(event: str, args: tuple[Any, ...]) -> None:
        if event.startswith("socket."):
            raise PermissionError("network access is disabled")
        if event in {
            "subprocess.Popen",
            "os.system",
            "os.posix_spawn",
            "os.fork",
            "os.forkpty",
            "os.spawn",
        }:
            raise PermissionError("child processes are disabled")
        if event == "open" and args:
            path = args[0]
            mode = args[1] if len(args) > 1 else "r"
            flags = args[2] if len(args) > 2 else 0
            writing = any(char in str(mode) for char in "wax+") or bool(
                isinstance(flags, int)
                and flags
                & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)
            )
            if writing and not _inside(path, root):
                raise PermissionError("writes outside the experiment directory are disabled")
        if event in {
            "os.remove",
            "os.rmdir",
            "os.mkdir",
            "os.rename",
            "os.replace",
            "os.symlink",
            "os.link",
        }:
            for path in args[:2]:
                if isinstance(path, (str, bytes, os.PathLike)) and not _inside(path, root):
                    raise PermissionError("filesystem mutation outside the experiment is disabled")

    sys.addaudithook(audit)

    def blocked(*_: Any, **__: Any) -> Any:
        raise PermissionError("network access is disabled")

    socket.create_connection = blocked  # type: ignore[assignment]
    socket.socket.connect = blocked  # type: ignore[assignment]
    socket.socket.connect_ex = blocked  # type: ignore[assignment]


def _install_temporary_path_mapping(root: Path) -> None:
    """Redirect benchmark ``/tmp`` fixtures into the isolated environment."""

    original_open = builtins.open
    original_io_open = io.open
    private_tmp = root / "tmp"

    def mapped_path(file: Any) -> Any:
        if not isinstance(file, (str, bytes, os.PathLike)):
            return file
        try:
            path = Path(os.fsdecode(file))
            relative = path.relative_to("/tmp")
        except (OSError, TypeError, ValueError):
            return file
        return private_tmp / relative

    def safe_open(file: Any, *args: Any, **kwargs: Any) -> Any:
        return original_open(mapped_path(file), *args, **kwargs)

    def safe_io_open(file: Any, *args: Any, **kwargs: Any) -> Any:
        return original_io_open(mapped_path(file), *args, **kwargs)

    builtins.open = safe_open  # type: ignore[assignment]
    io.open = safe_io_open  # type: ignore[assignment]


def _legacy_constant_class(
    name: str,
    predicate: Any,
) -> type:
    """Recreate removed AST aliases with their pre-3.14 isinstance semantics."""

    class LegacyConstantMeta(type):
        def __instancecheck__(cls, instance: Any) -> bool:
            return isinstance(instance, ast.Constant) and predicate(instance.value)

    class LegacyConstant(metaclass=LegacyConstantMeta):
        def __new__(cls, value: Any = None, **_: Any) -> ast.Constant:
            return ast.Constant(value=value)

    LegacyConstant.__name__ = name
    return LegacyConstant


def _install_ast_compatibility() -> None:
    """Support benchmark references written for the deprecated AST node API."""

    if not hasattr(ast.Constant(value=1), "n"):
        ast.Constant.n = property(  # type: ignore[attr-defined]
            lambda node: node.value,
            lambda node, value: setattr(node, "value", value),
        )
    if not hasattr(ast.Constant(value="text"), "s"):
        ast.Constant.s = property(  # type: ignore[attr-defined]
            lambda node: node.value,
            lambda node, value: setattr(node, "value", value),
        )
    aliases = {
        "Num": lambda value: isinstance(value, (int, float, complex))
        and not isinstance(value, bool),
        "Str": lambda value: isinstance(value, str),
        "Bytes": lambda value: isinstance(value, bytes),
        "NameConstant": lambda value: value is None or isinstance(value, bool),
        "Ellipsis": lambda value: value is Ellipsis,
    }
    for name, predicate in aliases.items():
        if not hasattr(ast, name):
            setattr(ast, name, _legacy_constant_class(name, predicate))


def _virtual_command_output(command: Any) -> str:
    """Return deterministic output for the benchmark's small command fixture."""

    if isinstance(command, str):
        parts = shlex.split(command)
    elif isinstance(command, (list, tuple)):
        parts = [os.fsdecode(part) for part in command]
    else:
        raise PermissionError("command must be a string or argument list")
    if not parts or any(any(char in part for char in ";&|`$<>()") for part in parts):
        raise PermissionError("command contains shell syntax")
    if parts[0] == "echo":
        return " ".join(parts[1:]) + "\n"
    if parts == ["ls", "-l"]:
        return "total 0\n"
    if parts == ["cat", "/etc/passwd"]:
        return "root:x:0:0:root:/root:/bin/sh\n"
    if parts == ["cat", "/dev/null"]:
        return ""
    raise PermissionError("command is not in the benchmark allowlist")


def _install_safe_command_stubs() -> None:
    """Virtualize the commands required by CWE-77 tests without spawning."""

    def safe_popen(
        command: str,
        mode: str = "r",
        buffering: int = -1,
    ) -> io.StringIO:
        del buffering
        if mode != "r":
            raise PermissionError("virtual commands are read-only")
        return io.StringIO(_virtual_command_output(command))

    def safe_check_output(command: Any, *_: Any, **kwargs: Any) -> str | bytes:
        if kwargs.get("shell"):
            raise PermissionError("shell execution is disabled")
        output = _virtual_command_output(command)
        if kwargs.get("text") or kwargs.get("universal_newlines") or kwargs.get("encoding"):
            return output
        return output.encode(kwargs.get("encoding") or "utf-8")

    os.popen = safe_popen  # type: ignore[assignment]
    subprocess.check_output = safe_check_output  # type: ignore[assignment]


def _deep_equal(actual: Any, expected: Any) -> bool:
    try:
        import numpy as np

        if isinstance(actual, np.ndarray) or isinstance(expected, np.ndarray):
            try:
                return bool(np.array_equal(actual, expected, equal_nan=True))
            except TypeError:
                return bool(np.array_equal(actual, expected))
    except ImportError:
        pass
    if isinstance(expected, dict) and isinstance(actual, dict):
        return expected.keys() == actual.keys() and all(
            _deep_equal(actual[key], value) for key, value in expected.items()
        )
    if isinstance(expected, (list, tuple)) and isinstance(actual, type(expected)):
        return len(actual) == len(expected) and all(
            _deep_equal(left, right) for left, right in zip(actual, expected)
        )
    if isinstance(expected, set) and isinstance(actual, set):
        return actual == expected
    try:
        result = actual == expected
        return bool(result)
    except (TypeError, ValueError):
        return False


def _safe_repr(value: Any) -> str:
    try:
        rendered = repr(value)
    except Exception:
        rendered = f"<{type(value).__name__}>"
    return rendered[:4000]


def _load(payload: dict[str, str]) -> dict[str, Any]:
    module = types.ModuleType("__generated__")
    sys.modules[module.__name__] = module
    namespace = module.__dict__
    exec(compile(payload["setup"], "<setup>", "exec"), namespace)
    exec(compile(payload["testcases"], "<testcases>", "exec"), namespace)
    exec(compile(payload["code"], "<generated>", "exec"), namespace)
    return namespace


def _run_case(payload: dict[str, str], category: str, index: int) -> dict[str, Any]:
    started = time.perf_counter()
    namespace = _load(payload)
    function = namespace.get(payload["function_name"])
    if not callable(function):
        raise RuntimeError(f"function not found: {payload['function_name']}")
    kwargs, expected = namespace["testcases"][category][index]
    expects_exception = isinstance(expected, type) and issubclass(expected, BaseException)
    actual: Any = None
    try:
        actual = function(**kwargs)
    except BaseException as exc:
        if expects_exception and isinstance(exc, expected):
            return {
                "passed": True,
                "status": "passed_expected_exception",
                "expected": expected.__name__,
                "actual": type(exc).__name__,
                "error": None,
                "duration_ms": (time.perf_counter() - started) * 1000,
            }
        return {
            "passed": False,
            "status": "unexpected_exception",
            "expected": expected.__name__ if expects_exception else _safe_repr(expected),
            "actual": type(exc).__name__,
            "error": f"{type(exc).__name__}: {exc}",
            "duration_ms": (time.perf_counter() - started) * 1000,
        }
    passed = not expects_exception and _deep_equal(actual, expected)
    return {
        "passed": passed,
        "status": "passed" if passed else ("missing_exception" if expects_exception else "wrong_value"),
        "expected": expected.__name__ if expects_exception else _safe_repr(expected),
        "actual": _safe_repr(actual),
        "error": None,
        "duration_ms": (time.perf_counter() - started) * 1000,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", type=Path)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--category")
    parser.add_argument("--index", type=int)
    args = parser.parse_args()
    payload = json.loads(args.payload.read_text(encoding="utf-8"))
    _install_guards(args.root.resolve())
    _install_temporary_path_mapping(args.root.resolve())
    _install_ast_compatibility()
    _install_safe_command_stubs()
    captured = io.StringIO()
    try:
        with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
            if args.list:
                namespace = _load(payload)
                testcases = namespace.get("testcases", {})
                result = {
                    "counts": {
                        "capability": len(testcases.get("capability", [])),
                        "safety": len(testcases.get("safety", [])),
                    }
                }
            else:
                result = _run_case(payload, args.category, args.index)
    except SyntaxError as exc:
        result = {"worker_error": "syntax_error", "error": f"{type(exc).__name__}: {exc}"}
    except ImportError as exc:
        result = {"worker_error": "import_error", "error": f"{type(exc).__name__}: {exc}"}
    except BaseException as exc:
        result = {"worker_error": "runtime_error", "error": f"{type(exc).__name__}: {exc}"}
    result["captured_output"] = captured.getvalue()[:4000]
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
