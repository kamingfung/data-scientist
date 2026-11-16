# Pipeline Conventions

Framework-agnostic rules for adding, wiring, and naming data and ML pipelines (applies to Kedro, Dagster, Prefect, Airflow, Hamilton, or plain Python orchestrators). For parameter injection, see [parameters.md](parameters.md). For schema validation at task/node boundaries, see [schema_validation.md](schema_validation.md).

## 1. Pipeline & Data Layers

Each pipeline layer has a single responsibility and writes to a distinct `data/` tier. Layers `01_raw`–`04_feature` are shared infrastructure; `05_model_input` onward are scoped to a specific model or report.

| Layer | Responsibility | Data directory | Granularity |
| --- | --- | --- | --- |
| **Ingestion** | Standardize column names, cast types, parse strings, remove invalid rows; no reshaping | `01_raw` -> `02_intermediate` | Source grain |
| **Preprocessing** | Align grains, join cleaned sources, validate core contracts | `03_primary` | Entity / time grain |
| **Feature Engineering** | Derive ratios, lags, rolling stats, and interactions from `03_primary` | `04_feature` | Same as preprocessing |
| **Modeling Input** | Assemble and filter model-specific training/inference tables | `05_model_input` | Model-specific |
| **Modeling** | Train/evaluate models and generate predictions | `06_models` + `07_model_output` | Predictions |
| **Reporting** | Aggregate and format outputs for dashboards, exports, and tracking | `08_reporting` | Consumer-specific |

## 2. Pipeline Package Structure

Each domain lives in its own package under `src/project_template/pipelines/`:

```text
src/project_template/
├── pipeline_registry.py  ← registers all domain pipelines
└── pipelines/
    ├── data_processing/
    │   ├── __init__.py
    │   ├── nodes.py      ← pure functions, one per node
    │   ├── pipeline.py   ← create_pipeline() wiring only
    │   └── schemas.py    ← Pandera schemas
    └── reporting/
        ├── __init__.py
        ├── nodes.py
        └── pipeline.py
```

- **Task/node functions live in `nodes.py` (or `tasks.py`); wiring lives in `pipeline.py`.** Never put transformation logic inside the DAG wiring file.
- **Task/node functions are pure:** the orchestrator injects all datasets and parameters; never read files or call `catalog.load()` inside a transform function, and never duplicate orchestrator start/finish logs (see [logging.md](logging.md)).

## 3. Naming, Wiring & Tags

- Expose a clear pipeline entrypoint per domain (e.g. `create_pipeline(**kwargs) -> Pipeline`, `@job`, or `@flow`).
- Name every task/node after its function (`name="preprocess_companies"`) so runner logs, profiling tables, and DAG UIs stay unambiguous. Never use generic names like `"step_1"`.
- Bind arguments explicitly by name (e.g. a dict of `inputs`) whenever positional order is non-obvious.
- Tag tasks/nodes with their domain (`tags=["data_processing"]`) so subsets can be executed independently.

## 4. Adding a New Pipeline

1. Create a domain module/package (e.g. `src/<project>/pipelines/<domain>/`) with pure transform functions (`nodes.py` / `tasks.py`), DAG wiring (`pipeline.py`), and Pandera contracts (`schemas.py`).
2. Register dataset I/O entries (using Parquet for intermediate tables).
3. Add parameters in the domain config (nested under `<domain>:`).
4. Register the pipeline in the project's pipeline registry or entrypoint.
5. Add unit tests under `tests/pipelines/<domain>/`.

## 5. Running Pipelines

Standardize common operations behind a `justfile` or `Makefile` regardless of orchestrator (example using Kedro + `uv` + MLflow):

```zsh
just run                                    # Run default pipeline (uv run kedro run)
just run --pipeline=data_processing         # Run one registered pipeline
just run --nodes=preprocess_companies_node  # Run a single node
just run --tags=data_processing             # Run nodes matching a tag
just run --runner=ThreadRunner              # Run independent nodes concurrently
just viz                                    # Launch interactive Kedro-Viz DAG viewer
just mlflow-local                           # Launch MLflow UI against sqlite:///mlflow.db
```
