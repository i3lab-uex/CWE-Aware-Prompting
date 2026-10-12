# CWE-Aware Prompting

Code and data for the paper **"Assessing the Proper Abstraction Level of
Security Knowledge for Code Generation"**.

**Does the CWE abstraction level used in a prompt change the security of LLM-generated code?**

This repository contains the pipeline, raw data and statistical analysis of the
controlled prompting experiment reported in the paper. Every prompt uses the same task template and
asks the model to consider security. The CWE conditions add a single hint: the
ID, name and description of one weakness taken from the target's lineage in the
[CWE hierarchy](https://cwe.mitre.org/data/definitions/1000.html).

| Condition  | CWE hint added to the prompt                  |
| ---------- | --------------------------------------------- |
| `Generic`  | None (generic security instruction only)      |
| `Pillar`   | The most abstract ancestor of the target CWE  |
| `Class`    | A Class-level weakness from the lineage       |
| `Base`     | A Base-level weakness from the lineage        |
| `Variant`  | A Variant-level weakness from the lineage     |
| `Compound` | A Compound weakness from the lineage          |

The generated code is then checked with **functional tests** (capability and
safety) and with **static analysis** (Bandit and CodeQL).

## Experiment at a glance

|                     |                                                        |
| ------------------- | ------------------------------------------------------ |
| Dataset             | SeCodePLT (insecure coding split): 819 tasks with tests, 17 target CWEs |
| Model               | `openai/gpt-oss-20b` (reasoning `low`, temperature 0.8) |
| Prompt combinations | 3,023 task × condition pairs                           |
| Generations         | 5 per pair, **15,115 in total**                        |
| Evaluation          | Capability tests, safety tests, Bandit, CodeQL         |
| Statistics          | Task-matched GLMMs with a random intercept per task, Holm-corrected |

## Key findings

- **Class-level prompts are the only ones with a significant effect.** Compared
  with `Generic`, they:
  - increase the overall test success rate (RR = 1.44),
  - increase safety-test success among functional code (RR = 1.17),
  - reduce the presence of the target CWE among functional code (RR = 0.20).
- **No level improves functional correctness**, and there is no monotonic trend
  across abstraction levels.
- The effects hold in a sensitivity analysis on the 475 tasks that have
  `Generic`, `Pillar`, `Class` and `Base` prompts.

The full report (in Spanish) is in
[`analysis/ReSAISE/informe_analisis_estadistico.md`](analysis/ReSAISE/informe_analisis_estadistico.md).

## Repository layout

```text
.
├── cwe_experiment/       # Generation, test execution and static analysis pipeline
├── utils/                # CWE hierarchy and prompt construction
├── data/
│   ├── insecure_coding-00000-of-00001.parquet   # SeCodePLT tasks
│   └── 1000.xml.zip                             # MITRE CWE View 1000 (v4.20)
├── experiments/
│   └── ReSAISE-20b/      # Raw run: results.parquet, manifest, Bandit/CodeQL reports, logs
├── analysis/
│   ├── ReSAISE/                  # Statistical analysis: tables, figures, report
│   ├── ReSAISE_sensitivity_CWE/  # Per-CWE sensitivity analysis
│   └── data-distribution/        # Dataset and design audit
├── scripts/              # Environment setup and CodeQL wrapper
├── tests/
├── experiment.py         # Experiment CLI (run / view)
├── run_experiment.sh     # Launcher for a full run
├── statistical_analysis.py
└── analyze_distribution.py
```

## Getting started

Requirements: Python 3.14, [uv](https://docs.astral.sh/uv/) and the CodeQL CLI.

```bash
./scripts/setup.sh   # creates .venv, installs CodeQL and runs the tests
```

### Reproduce the analysis

Everything needed is already in `experiments/ReSAISE-20b`:

```bash
uv run python statistical_analysis.py \
  --results experiments/ReSAISE-20b \
  --output-dir analysis/ReSAISE

uv run python analyze_distribution.py --output-dir analysis/data-distribution
```

### Run a new experiment

Any OpenAI-compatible endpoint (OpenAI, LM Studio, vLLM, …) can be used:

```bash
export OPENAI_API_KEY="your-key"
export BASE_URL="http://localhost:1234/v1"
export MODEL="openai/gpt-oss-20b"
export TEMPERATURE="0.8"
export REASONING="low"
export N="5"
./run_experiment.sh
```

Runs are stored under `experiments/<run-name>/` and can be resumed from their
checkpoints. Use `uv run python experiment.py run --help` for all options.

### Browse the results

```bash
uv run python experiment.py view --results experiments/ReSAISE-20b/results.parquet
```

This starts a local viewer to filter generations and inspect each prompt, the
model's reasoning, the generated code, test results and analyzer findings.

## Data sources

- **SeCodePLT**: Python coding tasks with capability and safety tests.
- **MITRE CWE View 1000** (Research Concepts, CWE List 4.20, 2026-04-30),
  SHA-256 `381838359c971649e4cf074a7d9bee800d724c564f81ebbfd5ee0eadd6c85e90`.

> Note: "no findings" from Bandit or CodeQL means only that the analyzers
> reported nothing; it is not proof that the code is secure.
