"""Deterministic local Spark 3.5.7 lab. Run with Python 3.10–3.12 and Java 17."""
import tempfile
import re
from pathlib import Path
from pyspark.sql import SparkSession, functions as F

spark = (SparkSession.builder.master("local[2]").appName("orders-learning-lab")
         .config("spark.sql.shuffle.partitions", "4")
         .config("spark.sql.adaptive.enabled", "true").getOrCreate())
spark.sparkContext.setLogLevel("WARN")
try:
    with tempfile.TemporaryDirectory(prefix="spark-orders-") as directory:
        path = str(Path(directory) / "orders")
        orders = spark.createDataFrame([
            (1, "telecom", 120, "2026-11-14"),
            (2, "telecom", 80, "2026-11-14"),
            (3, "banking", 200, "2026-11-14"),
            (4, "telecom", 50, "2026-11-15"),
        ], "order_id long, sector string, amount long, day string")
        orders.write.partitionBy("day").parquet(path)
        selected = (spark.read.parquet(path)
                    .where((F.col("day") == "2026-11-14") & (F.col("amount") >= 100))
                    .select("sector", "amount"))
        dimensions = spark.createDataFrame([("telecom", "Networks"), ("banking", "Finance")],
                                           "sector string, team string")
        joined = selected.join(F.broadcast(dimensions), "sector")
        totals = joined.groupBy("team").agg(F.sum("amount").alias("total"))
        print("PHYSICAL PLAN (inspect FileScan, PartitionFilters, PushedFilters, BroadcastHashJoin, Exchange):")
        totals.explain(mode="formatted")
        result = {row.team: row.total for row in totals.collect()}
        assert result == {"Networks": 120, "Finance": 200}, result
        plan = totals._jdf.queryExecution().executedPlan().toString()
        for marker in ("BroadcastHashJoin", "PartitionFilters", "PushedFilters", "Exchange"):
            assert marker in plan, f"Expected {marker} in physical plan"
        assert re.search(r"PartitionFilters: \[[^\]]*2026-11-14", plan), plan
        assert re.search(r"PushedFilters: \[[^\]]*GreaterThanOrEqual\(amount,100\)", plan), plan
        assert "ReadSchema: struct<sector:string,amount:bigint>" in plan, plan
        print("PASS: Finance=200, Networks=120; plan includes pruning, pushdown, broadcast, shuffle")
finally:
    spark.stop()
