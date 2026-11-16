# Parallelism & Threading

Rules for running data and ML pipelines concurrently without thread oversubscription or native-library segmentation faults.

## 1. The OpenMP + Threaded Runner Problem

Libraries backed by OpenMP (LightGBM, XGBoost, scikit-learn) spawn internal C++ thread pools when `n_jobs=-1`. Threaded task runners (such as `ThreadPoolExecutor`, Kedro's `ThreadRunner`, or threaded Dagster/Prefect executors) execute independent tasks concurrently across Python threads inside a single process.

Initializing OpenMP thread pools simultaneously from multiple Python threads can crash the process with a segmentation fault (`SIGSEGV` in `__kmp_suspend_initialize_thread`) or oversubscribe CPU cores (`N_tasks × N_cores` threads).

## 2. Core Rules

- **Pick one level of parallelism — never both at once.**
- **Cap `OMP_NUM_THREADS`** in the environment (or runner config) when running under a threaded runner.
- **Pass `n_jobs=1` on individual estimators** (`LGBMRegressor`, `XGBRegressor`, `RandomForestRegressor`, `GridSearchCV`) when parallelizing across tasks (threaded runner) or across outer model fits (`fit_n_jobs`).
- **Make hooks and shared utilities thread-safe:** protect shared counters and dictionaries in runner hooks or callbacks with `threading.Lock()`.

| Strategy | Runner | Outer `fit_n_jobs` | Estimator `n_jobs` | When to use |
| --- | --- | --- | --- | --- |
| Task + outer fit | Threaded (`ThreadPoolExecutor` / `ThreadRunner`) | `cores // concurrent_tasks` | `1` | Default for multi-task / multi-target pipelines |
| Task-level only | Threaded (`ThreadPoolExecutor` / `ThreadRunner`) | `1` | `1` | Debugging concurrent tasks with deterministic traces |
| Model-level | Sequential (`SequentialRunner`) | `1` | `-1` | Single heavy model fit on a large dataset |
| Process-level | Multi-process (`ProcessPoolExecutor` / `ParallelRunner`) | `1` | `-1` | Separate OS processes (requires serializable/persisted datasets such as Parquet) |

```python
# Good — safe inside threaded runners
model = LGBMRegressor(
    random_state=42, n_jobs=1, deterministic=True, force_row_wise=True
)

# Bad — spawns OpenMP thread pools inside Python threads
model = LGBMRegressor(random_state=42, n_jobs=-1)
```

## 3. Container CPU Limits

`multiprocessing.cpu_count()` reports the **host** machine's core count, not a container's cgroup vCPU quota. In containerized batch jobs, read the allocated vCPU budget from an explicit environment variable (or `os.process_cpu_count()` in Python 3.13+) before sizing thread pools.
