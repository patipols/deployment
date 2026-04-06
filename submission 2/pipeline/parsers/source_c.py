import pandas as pd
import hashlib
from utils.helper import to_float

def parse_source_c(file_path):

    df = pd.read_excel(file_path)
    df["timestamp"] = pd.to_datetime(df["GPS_TIME"], errors="coerce")

    df["record_id"] = df.apply(
        lambda r: hashlib.md5(f"{r['IMEI']}_{r['timestamp']}".encode()).hexdigest(),
        axis=1
    )

    return pd.DataFrame({
        "record_id": df["record_id"],
        "source": "source_c",
        "vehicle_id": df["TKNO"].astype(str),
        "timestamp": df["timestamp"],
        "lat": df["LATITUDE"].apply(to_float),
        "lon": df["LONGITUDE"].apply(to_float),
        "speed": df["SPEED"].apply(to_float),
        "heading": df["DIRECTION"].apply(to_float),
        "engine_status": df["ENGINE_STATUS"].astype(str),
        "fuel_level": None,
        "fuel_rate": None,
        "mileage": None,
        "altitude": df["ALTITUDE"].apply(to_float),
        "raw_event_type": None,
        "ingestion_time": pd.Timestamp.now()
    })