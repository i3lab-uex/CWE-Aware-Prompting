import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

import pytest

from main import BanditError, find_cwes, main


def bandit_result(results: list[object]) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout=json.dumps({"results": results}),
        stderr="",
    )


def test_find_cwes_returns_empty_list_when_no_issues(tmp_path: Path) -> None:
    with patch("main.subprocess.run", return_value=bandit_result([])) as run:
        assert find_cwes(tmp_path) == []

    run.assert_called_once_with(
        [
            sys.executable,
            "-m",
            "bandit",
            "-r",
            str(tmp_path),
            "-f",
            "json",
            "-q",
            "--exit-zero",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_find_cwes_deduplicates_and_sorts_by_task_and_cwe(tmp_path: Path) -> None:
    findings = [
        {"filename": "/scan/task_b.py", "issue_cwe": {"id": 89}},
        {"filename": "/scan/task_a.py", "issue_cwe": {"id": 78}},
        {"filename": "/scan/task_a.py", "issue_cwe": {"id": 22}},
        {"filename": "/scan/task_a.py", "issue_cwe": {"id": 78}},
        {"filename": "/other/task_b.py", "issue_cwe": {"id": 89}},
    ]

    with patch("main.subprocess.run", return_value=bandit_result(findings)):
        assert find_cwes(tmp_path) == [
            {"task_id": "task_a", "cwe_id": 22},
            {"task_id": "task_a", "cwe_id": 78},
            {"task_id": "task_b", "cwe_id": 89},
        ]


def test_find_cwes_keeps_same_cwe_for_different_tasks(tmp_path: Path) -> None:
    findings = [
        {"filename": "first.py", "issue_cwe": {"id": 78}},
        {"filename": "second.py", "issue_cwe": {"id": 78}},
    ]

    with patch("main.subprocess.run", return_value=bandit_result(findings)):
        assert find_cwes(tmp_path) == [
            {"task_id": "first", "cwe_id": 78},
            {"task_id": "second", "cwe_id": 78},
        ]


def test_find_cwes_rejects_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="no existe"):
        find_cwes(tmp_path / "missing")


def test_find_cwes_rejects_file(tmp_path: Path) -> None:
    file_path = tmp_path / "task.py"
    file_path.write_text("pass", encoding="utf-8")

    with pytest.raises(NotADirectoryError, match="no es un directorio"):
        find_cwes(file_path)


def test_find_cwes_reports_bandit_failure(tmp_path: Path) -> None:
    failure = subprocess.CompletedProcess(
        args=[], returncode=2, stdout="", stderr="configuration error"
    )

    with patch("main.subprocess.run", return_value=failure):
        with pytest.raises(BanditError, match="configuration error"):
            find_cwes(tmp_path)


def test_find_cwes_rejects_invalid_json(tmp_path: Path) -> None:
    invalid = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="not-json", stderr=""
    )

    with patch("main.subprocess.run", return_value=invalid):
        with pytest.raises(BanditError, match="JSON válido"):
            find_cwes(tmp_path)


def test_main_prints_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    findings = [{"filename": "task_1.py", "issue_cwe": {"id": 78}}]

    with patch("main.subprocess.run", return_value=bandit_result(findings)):
        assert main([str(tmp_path)]) == None
        
    captured = capsys.readouterr()
    assert json.loads(captured.out) == [{"task_id": "task_1", "cwe_id": 78}]
    assert captured.err == ""


def test_main_raises_descriptive_error_for_missing_directory(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    with pytest.raises(Exception, match=f"Error al analizar {missing}"):
        main([str(missing)])


def test_find_cwes_with_mock_examples() -> None:
    mock_directory = Path(__file__).parent.parent / "tests" / "mocks"

    assert find_cwes(mock_directory) == [
        {"task_id": "assert_usage", "cwe_id": 703},
        {"task_id": "command_injection", "cwe_id": 78},
    ]
