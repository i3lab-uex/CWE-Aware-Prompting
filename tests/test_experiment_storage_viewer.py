import json
from pathlib import Path
from urllib.request import urlopen
import threading
import pytest

from cwe_experiment.storage import FragmentStore, read_parquet, result_schema
from cwe_experiment.viewer import ResultRepository, create_server


def row(task: str, level: str, index: int, *, passed: bool = False) -> dict:
    value = {name: None for name in result_schema().names}
    value.update(
        run_id="run",
        task_id=task,
        target_cwe=78,
        cwe_level=level,
        generation_index=index,
        model="fake",
        syntax_valid=True,
        test_total=1,
        test_passed=int(passed),
        all_tests_pass=passed,
        any_cwe_detected=False,
        reasoning_summaries=[{"type": "summary_text", "text": "summary"}],
        codeql_suites=["stable", "experimental"],
        test_results=[
            {
                "category": "capability",
                "test_index": 0,
                "passed": passed,
                "status": "passed" if passed else "wrong_value",
                "expected": "1",
                "actual": "1" if passed else "0",
                "error": None,
                "duration_ms": 1.0,
            }
        ],
        bandit_status="complete",
        codeql_status="unavailable",
        bandit_findings=[],
        codeql_findings=[],
    )
    return value


def test_nested_parquet_round_trip_and_resume(tmp_path: Path) -> None:
    output = tmp_path / "results.parquet"
    store = FragmentStore(output, config={"model": "fake"})
    store.write(row("b", "Base", 0, passed=True))
    store.write(row("a", "Generic", 0))
    # The same key is updated rather than duplicated.
    store.write(row("a", "Generic", 0, passed=True))
    store.compact()

    rows = read_parquet(output)
    assert [(item["task_id"], item["cwe_level"]) for item in rows] == [
        ("a", "Generic"),
        ("b", "Base"),
    ]
    assert rows[0]["reasoning_summaries"][0]["text"] == "summary"
    assert rows[0]["test_results"][0]["passed"] is True
    resumed = FragmentStore(output, config={"model": "fake"})
    assert len(resumed.by_key()) == 2


def test_later_batch_stage_replaces_earlier_stage(tmp_path: Path) -> None:
    output = tmp_path / "staged.parquet"
    store = FragmentStore(output, config={"model": "fake"})
    store.write_batch("generation", 0, [row("task", "Generic", 0)])
    store.write_batch("evaluation", 0, [row("task", "Generic", 0, passed=True)])

    assert len(store.rows()) == 1
    assert store.rows()[0]["all_tests_pass"] is True


def test_run_manifest_separates_unique_id_from_config_hash(tmp_path: Path) -> None:
    first = FragmentStore(
        tmp_path / "first" / "results.parquet",
        config={"output": str(tmp_path / "first" / "results.parquet"), "model": "fake"},
    )
    second = FragmentStore(
        tmp_path / "second" / "results.parquet",
        config={"output": str(tmp_path / "second" / "results.parquet"), "model": "fake"},
    )

    assert first.fingerprint == second.fingerprint
    assert first.run_id != second.run_id
    assert first.manifest_path == tmp_path / "first" / "manifest.json"
    assert first.directory == tmp_path / "first" / "checkpoints"
    assert first.logs_directory.is_dir()
    assert first.reports_directory.is_dir()
    assert first.failures_directory.is_dir()

    first.mark_complete(rows=0)
    resumed = FragmentStore(
        tmp_path / "first" / "results.parquet",
        config={"output": str(tmp_path / "first" / "results.parquet"), "model": "fake"},
    )
    assert resumed.run_id == first.run_id
    assert resumed.manifest["resume_count"] == 1
    assert resumed.manifest["status"] == "running"


def test_missing_default_reasoning_field_keeps_old_run_resumable(tmp_path: Path) -> None:
    output = tmp_path / "legacy" / "results.parquet"
    original = FragmentStore(output, config={"model": "fake"})

    resumed = FragmentStore(
        output,
        config={"model": "fake", "reasoning_effort": None},
    )

    assert resumed.run_id == original.run_id


def test_concurrency_can_change_when_resuming_and_is_recorded(tmp_path: Path) -> None:
    output = tmp_path / "resumable" / "results.parquet"
    original = FragmentStore(
        output,
        config={"output": str(output), "model": "fake", "concurrency": 50},
    )

    resumed = FragmentStore(
        output,
        config={"output": str(output), "model": "fake", "concurrency": 20},
    )

    assert resumed.run_id == original.run_id
    assert resumed.fingerprint == original.fingerprint
    assert resumed.manifest["config"]["concurrency"] == 20
    assert resumed.manifest["execution_history"] == [
        {
            "started_at": original.manifest["started_at"],
            "resume_count": 0,
            "concurrency": 50,
        },
        {
            "started_at": resumed.manifest["last_resumed_at"],
            "resume_count": 1,
            "concurrency": 20,
        },
    ]
    events = [
        json.loads(line)
        for line in resumed.events_path.read_text(encoding="utf-8").splitlines()
    ]
    assert events[-1]["operational_changes"] == {
        "concurrency": {"previous": 50, "current": 20}
    }


def test_semantic_configuration_still_cannot_change_when_resuming(tmp_path: Path) -> None:
    output = tmp_path / "protected" / "results.parquet"
    FragmentStore(
        output,
        config={"output": str(output), "model": "first", "concurrency": 50},
    )

    with pytest.raises(RuntimeError, match="otra configuración"):
        FragmentStore(
            output,
            config={"output": str(output), "model": "second", "concurrency": 20},
        )


def test_viewer_filters_paginates_and_serves_endpoints(tmp_path: Path) -> None:
    output = tmp_path / "results.parquet"
    store = FragmentStore(output, config={"model": "fake"})
    store.write(row("first", "Generic", 0, passed=True))
    store.write(row("second", "Base", 0))
    store.compact()
    repository = ResultRepository(output)

    assert repository.meta()["total"] == 2
    result = repository.query({"functional": ["pass"], "page_size": ["1"]})
    assert result["total"] == 1
    assert result["items"][0]["task_id"] == "first"

    try:
        server = create_server(output, port=0)
    except PermissionError:
        pytest.skip("The test sandbox forbids binding a loopback socket")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = f"http://127.0.0.1:{server.server_port}"
        with urlopen(base + "/api/meta") as response:
            assert json.load(response)["total"] == 2
        with urlopen(base + "/api/results?page=1&page_size=1") as response:
            assert json.load(response)["pages"] == 2
        with urlopen(base + "/") as response:
            assert b"CWE abstraction experiment" in response.read()
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
