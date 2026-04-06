import json
import pandas as pd
import hashlib
from utils.helper import to_float

def parse_source_a(file_path):

    with open(file_path) as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["local_timestamp"], errors="coerce")

    df["record_id"] = df.apply(
        lambda r: hashlib.md5(
            f"{r['registration']}_{r['timestamp']}_{r['lat']}_{r['lon']}".encode()
        ).hexdigest(),
        axis=1
    )

    return pd.DataFrame({
        "record_id": df["record_id"],
        "source": "source_a",
        "vehicle_id": df["registration"].astype(str),
        "timestamp": df["timestamp"],
        "lat": df["lat"].apply(to_float),
        "lon": df["lon"].apply(to_float),
        "speed": df["speed"].apply(to_float),
        "heading": df["course"].apply(to_float),
        "engine_status": None,
        "fuel_level": df["fuel_sensor"].apply(to_float),
        "fuel_rate": df["fuel_canbus"].apply(to_float),
        "mileage": df["mileage"].apply(to_float),
        "altitude": None,
        "raw_event_type": df["event_en"].astype(str),
        "ingestion_time": pd.Timestamp.now()
    })