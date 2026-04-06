import pandas as pd

def run(df_events):

    df_events = df_events.sort_values(["vehicle_id", "timestamp"])

    sessions = []

    for vehicle_id, group in df_events.groupby("vehicle_id"):
        start_time = None

        for _, row in group.iterrows():
            if row["event_type"] == "33":
                start_time = row["timestamp"]

            elif row["event_type"] == "34" and start_time:
                sessions.append({
                    "vehicle_id": vehicle_id,
                    "start_time": start_time,
                    "end_time": row["timestamp"]
                })
                start_time = None

        # missing OFF
        if start_time:
            sessions.append({
                "vehicle_id": vehicle_id,
                "start_time": start_time,
                "end_time": start_time + pd.Timedelta(hours=24)
            })

    result = pd.DataFrame(sessions)

    if not result.empty:
        result["duration_minutes"] = (
            result["end_time"] - result["start_time"]
        ).dt.total_seconds() / 60

    return result