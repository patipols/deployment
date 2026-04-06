# Mobility Insight — Data Engineering Assignment

## Overview

This project builds a simplified **Mobility Intelligence Platform** that ingests vehicle telemetry data from multiple sources, normalizes it into a unified schema, and enables analytics on top of a Parquet-based data lake.

---

## Architecture

```text
Raw Data → Ingestion (Python) → Unified Schema → Parquet → Analytics
```

---

## Key Design

### Unified Schema

* Single table for cross-source analytics (`unified.parquet`)
* Standard fields: `vehicle_id`, `timestamp`, `lat`, `lon`, `speed`
* Source-specific fields are nullable
* `source` column preserves lineage

---

### Toyota Data (Important)

Separated into 2 datasets:

* `toyota_events.parquet` → event-level (ON/OFF, speed)
* `toyota_timeseries.parquet` → per-second CAN signals

This enables both event-based and time-series analytics.

---

### Pipeline Design

* Modular structure (parsers, utils, orchestrator)
* Handles JSON + XLSX
* Validates data (geo bounds, speed)
* Deduplicates using `record_id` (idempotent)
* Flattens nested Toyota CAN data

---

### Storage

* Parquet format (columnar, efficient, scalable)
* Acts as a lightweight data lake

---

### Query Layer

* Queries implemented as modular Python functions
* Separate from ingestion (clean architecture)

---

## Analytics

### Query 1: Engine Sessions

* Reconstruct ON/OFF sessions from Toyota events
* Handles missing OFF (fallback 24h)

### Query 2: Idle Detection

* Detects idle > 30 minutes (speed = 0)
* Uses time-gap grouping

### Query 3: Cross-Source Validation

* Compares positions across sources
* Flags >1 km difference within 5 minutes

---

## Assumptions

* Simplified Toyota vehicle ID
* Missing OFF capped at 24 hours
* Input timestamps assumed consistent

---

## Limitations

* Batch pipeline only
* No partitioning
* No orchestration (e.g., Airflow)

---

## Future Improvements

* Partitioned Parquet (by date/vehicle)
* DuckDB/Spark for scalable querying
* Incremental ingestion
* Data quality monitoring

---

## How to Run

```bash
cd pipeline
python ingest.py

cd ../query
python run_queries.py
```

---

## Summary

This solution demonstrates:

* Multi-source data ingestion
* Handling nested telemetry (Toyota CAN)
* Idempotent pipeline design
* Analytics-ready data modeling
