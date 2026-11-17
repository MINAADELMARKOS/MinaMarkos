# PySpark orders and physical-plan lab

Supported tutorial baseline: **PySpark 3.5.7, Python 3.10–3.12, JDK 17**. Tested on Linux with Python 3.12.14, Temurin JDK 17.0.17, and `local[2]`. An additional local run also passed with the environment's Java 21, but JDK 17 is the documented baseline for Spark 3.5.

From the portfolio checkout, select a full JDK 17 through `JAVA_HOME`, then:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install pyspark==3.5.7
SPARK_LOCAL_IP=127.0.0.1 .venv/bin/python examples/spark/orders_lab.py
```

The fixture uses four synthetic orders and two dimension rows. It writes temporary partitioned Parquet, selects one day and eligible amounts, broadcasts a small dimension, aggregates by team, prints a formatted physical plan, asserts exact results and expected plan markers, and cleans up its temporary data.

Expected final line:

```text
PASS: Finance=200, Networks=120; plan includes pruning, pushdown, broadcast, shuffle
```

## What to inspect

- `PartitionFilters`: day-based directory pruning.
- `ReadSchema`: selected source columns (column pruning).
- `PushedFilters`: supported amount predicate passed to Parquet; not proof of a specific byte reduction.
- `BroadcastHashJoin`: explicit tiny build-side broadcast.
- `Exchange`: redistribution for grouped totals.
- `AdaptiveSparkPlan`: inspect the final plan after execution; details can change across Spark builds.

`local[2]` limits CPU use. Four shuffle partitions keep the teaching plan visible; they are not a production default. AQE is explicitly enabled. Integer amounts give exact assertions; use appropriate decimal semantics for real financial data.

## Troubleshooting and boundaries

Check `JAVA_HOME`, Java/Python compatibility, and the exact PySpark version if startup fails. Keep `SPARK_LOCAL_IP=127.0.0.1` for this local lab when hostname resolution is unavailable. A native Hadoop library warning alone does not invalidate these local Parquet results. Inspect the first exception if an action fails.

If a plan assertion fails on another runtime, inspect the actual plan and version before changing it. Do not remove the result assertions to get a passing output. This tiny fixture verifies semantics and plan features, not a performance gain, executor failure recovery, or Cloudera/cloud compatibility.

[Validation scope](../VALIDATION.md) · [Spark learning notes](https://github.com/MINAADELMARKOS/Apache_Spark) · [Earlier PySpark notebooks](https://github.com/MINAADELMARKOS/Pyspark-_Tutorials)
