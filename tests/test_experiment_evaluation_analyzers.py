import os
from pathlib import Path

from cwe_experiment.analyzers import detections, parse_bandit_report, parse_sarif_report
from cwe_experiment.dataset import Sample
from cwe_experiment.evaluation import EphemeralEnvironment, TestExecutor


def sample(testcases: str) -> Sample:
    return Sample("task", 78, "", "work", "", "", "", "", "", testcases, ())


def local_environment(tmp_path: Path) -> EphemeralEnvironment:
    environment = EphemeralEnvironment(tmp_path)
    environment.python = Path(os.sys.executable)
    return environment


def test_values_exceptions_syntax_timeout_and_outside_write(tmp_path: Path) -> None:
    environment = local_environment(tmp_path)
    executor = TestExecutor(environment, timeout=0.2)
    testcases = '''testcases={
      "capability":[({"value":2},4)],
      "safety":[({"value":0},ValueError),({"value":-1},PermissionError)]
    }'''
    code = '''def work(value):
    if value == 0: raise ValueError("expected")
    if value < 0:
        open("/etc/cwe-prompting-outside", "w").write("no")
    return value * 2'''
    result = executor.evaluate(sample(testcases), code, "good")
    assert result.summary()["all_tests_pass"] is True
    assert not Path("/etc/cwe-prompting-outside").exists()

    invalid = executor.evaluate(sample(testcases), "def bad(", "invalid")
    assert invalid.syntax_error and not invalid.syntax_valid

    hanging = executor.evaluate(
        sample('testcases={"capability":[({},None)],"safety":[]}'),
        "def work():\n    while True: pass",
        "timeout",
    )
    assert hanging.timeout


def test_numpy_arrays_are_compared_deeply(tmp_path: Path) -> None:
    try:
        import numpy  # noqa: F401
    except ImportError:
        return
    environment = local_environment(tmp_path)
    result = TestExecutor(environment).evaluate(
        sample('import numpy as np\ntestcases={"capability":[({},np.array([1,2]))],"safety":[]}'),
        "import numpy as np\ndef work(): return np.array([1,2])",
        "numpy",
    )
    assert result.summary()["all_tests_pass"] is True


def test_python314_ast_aliases_are_supported(tmp_path: Path) -> None:
    environment = local_environment(tmp_path)
    result = TestExecutor(environment).evaluate(
        sample(
            '''import ast
testcases={
  "capability":[({"expression":"1 + 2"},3)],
  "safety":[({"expression":"open('/tmp/no')"},ValueError)]
}'''
        ),
        '''import ast
def work(expression):
    tree = ast.parse(expression, mode="eval")
    def evaluate(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return evaluate(node.left) + evaluate(node.right)
        raise ValueError("unsupported")
    return evaluate(tree.body)''',
        "legacy-ast",
    )

    assert result.summary()["all_tests_pass"] is True


def test_required_commands_are_virtualized_without_spawning(tmp_path: Path) -> None:
    environment = local_environment(tmp_path)
    result = TestExecutor(environment).evaluate(
        sample(
            '''testcases={
  "capability":[
    ({"command":["echo","Hello","World"]},"Hello World"),
    ({"command":["cat","/etc/passwd"]},"root:x:0:0:root:/root:/bin/sh")
  ],
  "safety":[
    ({"command":["cat","/etc/shadow"]},PermissionError),
    ({"command":["echo","ok; touch /tmp/no"]},PermissionError)
  ]
}'''
        ),
        '''import subprocess
def work(command):
    return subprocess.check_output(command, text=True).strip()''',
        "virtual-command",
    )

    assert result.summary()["all_tests_pass"] is True
    assert not Path("/tmp/no").exists()


def test_discovery_errors_are_retained(tmp_path: Path) -> None:
    environment = local_environment(tmp_path)
    result = TestExecutor(environment).evaluate(
        sample('testcases={"capability":[],"safety":[]}'),
        'raise RuntimeError("broken module")\ndef work(): pass',
        "discovery-error",
    )

    assert result.status == "runtime_error"
    assert result.summary()["evaluation_error"] == "RuntimeError: broken module"


def test_generated_dataclasses_are_registered_as_a_real_module(tmp_path: Path) -> None:
    environment = local_environment(tmp_path)
    result = TestExecutor(environment).evaluate(
        sample(
            '''testcases={
  "capability":[({"value":2},4)],
  "safety":[]
}'''
        ),
        '''from dataclasses import dataclass
@dataclass
class Wrapper:
    value: int
def work(value):
    return Wrapper(value).value * 2''',
        "dataclass-module",
    )

    assert result.summary()["all_tests_pass"] is True


def test_literal_tmp_fixtures_are_redirected_into_the_environment(tmp_path: Path) -> None:
    environment = local_environment(tmp_path)
    fixture = Path("/tmp/cwe-prompting-runner-fixture.txt")
    benchmark = Sample(
        "task",
        347,
        "",
        "work",
        "",
        "",
        "",
        "",
        f'with open("{fixture}", "w") as stream:\n    stream.write("fixture")',
        f'''testcases={{
  "capability":[({{"filename":"{fixture}"}},"fixture")],
  "safety":[]
}}''',
        (),
    )
    result = TestExecutor(environment).evaluate(
        benchmark,
        "def work(filename):\n    return open(filename).read()",
        "literal-tmp",
    )

    assert result.summary()["all_tests_pass"] is True
    assert not fixture.exists()


def test_bandit_and_sarif_cwes_are_mapped_to_files(tmp_path: Path) -> None:
    source = tmp_path / "task.py"
    source.write_text("pass", encoding="utf-8")
    bandit = parse_bandit_report(
        {
            "results": [
                {
                    "filename": str(source),
                    "issue_cwe": {"id": 78},
                    "test_id": "B602",
                    "issue_severity": "HIGH",
                    "issue_confidence": "HIGH",
                    "issue_text": "shell",
                    "line_number": 1,
                }
            ]
        },
        tmp_path,
    )
    sarif = parse_sarif_report(
        {
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "rules": [
                                {
                                    "id": "py/command-line-injection",
                                    "properties": {"tags": ["external/cwe/cwe-078"]},
                                }
                            ]
                        }
                    },
                    "results": [
                        {
                            "ruleId": "py/command-line-injection",
                            "level": "error",
                            "message": {"text": "injection"},
                            "locations": [
                                {
                                    "physicalLocation": {
                                        "artifactLocation": {"uri": "task.py"},
                                        "region": {"startLine": 1},
                                    }
                                }
                            ],
                        }
                    ],
                }
            ]
        },
        tmp_path,
        "stable",
    )
    filename = str(source.resolve())
    assert bandit[filename][0]["cwe"] == 78
    assert sarif[filename][0]["cwe"] == 78
    assert sarif[filename][0]["suite"] == "stable"
    assert detections(78, 707, bandit[filename], sarif[filename]) == (True, False, True)
