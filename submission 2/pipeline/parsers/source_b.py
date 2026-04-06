# pipeline/parsers/source_b.py

import json
import pandas as pd
import hashlib
from utils.helper import to_float

def parse_source_b(file_51, file_52):

    unified, events, timeseries = [], [], []

    def gen_id(vehicle_id, ts):
        return hashlib.md5(f"{vehicle_id}_{ts}".encode()).hexdigest()

    # =====================
    # 0x51 FILE
    # =====================
    with open(file_51) as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]

    for rec in data:
        try:
            gps = rec.get("Common header", {}).get("GPS", {})

            lat = to_float(gps.get("Lat angle"))
            lon = to_float(gps.get("Lon angle"))
            ts = pd.to_datetime(gps.get("Timestamp"), errors="coerce")

            vehicle_id = "toyota_vehicle"
            event_list = rec.get("B2B Event List", [])

            for event in event_list:
                event_type = str(event.get("Event type"))
                speed = to_float(event.get("Vehicle speed"))

                event_id = gen_id(vehicle_id, ts)

                # ---------- Unified ----------
                unified.append({
                    "record_id": event_id,
                    "source": "toyota",
                    "vehicle_id": vehicle_id,
                    "timestamp": ts,
                    "lat": lat,
                    "lon": lon,
                    "speed": speed,
                    "heading": None,
                    "engine_status": None,
                    "fuel_level": None,
                    "fuel_rate": None,
                    "mileage": None,
                    "altitude": None,
                    "raw_event_type": event_type,
                    "ingestion_time": pd.Timestamp.now()
                })

                # ---------- Event ----------
                events.append({
                    "event_id": event_id,
                    "vehicle_id": vehicle_id,
                    "timestamp": ts,
                    "event_type": event_type,
                    "speed": speed
                })

            # ---------- Timeseries ----------
            contained = rec.get("Engine RPM information", {}).get("Contained data List", [])

            for entry in contained:
                for item in entry.get("CAN List", []):
                    ts_signal = pd.to_datetime(item.get("Timestamp"), errors="coerce")

                    for group in ["CAN", "WNG"]:
                        if group in item:
                            for k, v in item[group].items():
                                timeseries.append({
                                    "event_id": event_id,
                                    "signal_name": k,
                                    "signal_value": to_float(v),
                                    "signal_timestamp": ts_signal
                                })

        except Exception as e:
            print("Skip bad 0x51 record:", e)

    # =====================
    # 0x52 FILE
    # =====================
    with open(file_52) as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]

    for rec in data:
        try:
            event = rec.get("B2B event", {})
            gps = event.get("GPS", {})

            lat = to_float(gps.get("Lat angle"))
            lon = to_float(gps.get("Lon angle"))
            ts = pd.to_datetime(gps.get("Timestamp"), errors="coerce")

            vehicle_id = "toyota_vehicle"
            event_id = gen_id(vehicle_id, ts)

            events.append({
                "event_id": event_id,
                "vehicle_id": vehicle_id,
                "timestamp": ts,
                "event_type": "33",  # Engine ON
                "speed": to_float(event.get("Vehicle speed"))
            })

        except Exception as e:
            print("Skip bad 0x52 record:", e)

   
    return (
        pd.DataFrame(unified),
        pd.DataFrame(events),
        pd.DataFrame(timeseries)
    )