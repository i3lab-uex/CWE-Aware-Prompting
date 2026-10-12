import re

from cwe_experiment.dataset import load_samples
from cwe_experiment.prompts import build_prompt_conditions


FORBIDDEN_MARKERS = (
    "security_policy",
    "ground_truth",
    "patched_code",
    "vulnerable_code",
    "unittest",
)


def test_functional_coverage_and_condition_count() -> None:
    samples, coverage = load_samples()

    assert len(samples) == coverage.selected_samples == 819
    assert coverage.total_samples == 1345
    assert coverage.excluded_without_tests == 526
    assert len(coverage.selected_cwes) == 17
    assert sum(len(build_prompt_conditions(sample)) for sample in samples) == 3023


def test_prompts_do_not_leak_withheld_fields_or_multiple_cwes() -> None:
    samples, _ = load_samples()

    for sample in samples:
        conditions = build_prompt_conditions(sample)
        generic = conditions[0].prompt
        assert re.findall(r"CWE-\d+", generic, flags=re.IGNORECASE) == []
        if sample.setup:
            assert sample.setup not in generic
        if sample.testcases:
            assert sample.testcases not in generic
        assert all(marker not in generic for marker in FORBIDDEN_MARKERS)
        for condition in conditions[1:]:
            assert re.findall(r"CWE-(\d+)", condition.prompt, flags=re.IGNORECASE) == [
                str(condition.prompt_cwe)
            ]


def test_description_option_changes_only_the_cwe_suffix() -> None:
    sample = next(sample for sample in load_samples()[0] if sample.target_cwe == 95)
    plain = build_prompt_conditions(sample)
    detailed = build_prompt_conditions(sample, include_cwe_description=True)

    assert plain[0].prompt == detailed[0].prompt
    for left, right in zip(plain[1:], detailed[1:]):
        assert right.prompt.startswith(left.prompt)
        assert right.prompt != left.prompt
