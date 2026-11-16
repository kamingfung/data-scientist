# Developer Guidelines

Engineering standards for Python code, Kedro pipelines, tests, logging, visualization, and documentation.

| Guide | Audience & Scope |
| --- | --- |
| [code_style.md](code_style.md) | Pure functions, readability, top-down order, fail-loud error handling |
| [logging.md](logging.md) | Logger usage, mandatory log context, levels, lazy `%` formatting |
| [unit_test.md](unit_test.md) | Test structure, realistic fixtures, Pandera vs. unit tests, mocking rules |
| [pipeline.md](pipeline.md) | Kedro data layers, pipeline structure, node naming, adding pipelines |
| [parameters.md](parameters.md) | Parameter nesting, narrow slicing, strict access, YAML quoting |
| [schema_validation.md](schema_validation.md) | Pandera boundaries, tuple-coercion bug, dtype safety, Parquet |
| [visualization.md](visualization.md) | Colorblind-safe palettes, paired encodings, Mermaid vs. Graphviz |
| [writing_standards.md](writing_standards.md) | ASD-STE100 prose, terminology, reproducible evidence, markdown layout |
| [parallelism.md](parallelism.md) | Concurrency and parallelism patterns |
