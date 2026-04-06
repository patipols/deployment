-- Unified Telemetry Table

CREATE TABLE unified_telemetry (
    record_id STRING PRIMARY KEY,
    source STRING,                 -- source_a / toyota / source_c

    vehicle_id STRING,
    timestamp TIMESTAMP,

    -- Location
    lat DOUBLE,
    lon DOUBLE,
    altitude DOUBLE,

    -- Movement
    speed DOUBLE,
    heading DOUBLE,

    -- Engine / Status
    engine_status STRING,
    raw_event_type STRING,

    -- Fuel / Vehicle metrics
    fuel_level DOUBLE,
    fuel_rate DOUBLE,
    mileage DOUBLE,

    -- Metadata
    ingestion_time TIMESTAMP
);



-- Toyota Event Table

CREATE TABLE toyota_events (
    event_id STRING PRIMARY KEY,
    vehicle_id STRING,
    timestamp TIMESTAMP,
    event_type STRING,   -- 33=ON, 34=OFF, 30=heartbeat
    speed DOUBLE
);



-- Toyota CAN Timeseries Table

CREATE TABLE toyota_timeseries (
    event_id STRING,
    signal_name STRING,
    signal_value DOUBLE,
    signal_timestamp TIMESTAMP
);