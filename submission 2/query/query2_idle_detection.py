def run(df):

    df_idle = df[df["speed"] == 0].copy()
    df_idle = df_idle.sort_values(["vehicle_id", "timestamp"])

    df_idle["prev_time"] = df_idle.groupby("vehicle_id")["timestamp"].shift(1)

    df_idle["gap"] = (
        df_idle["timestamp"] - df_idle["prev_time"]
    ).dt.total_seconds()

    df_idle["new_group"] = (df_idle["gap"] > 120).astype(int)

    df_idle["grp"] = df_idle.groupby("vehicle_id")["new_group"].cumsum()

    result = df_idle.groupby(["vehicle_id", "grp"]).agg(
        idle_start=("timestamp", "min"),
        idle_end=("timestamp", "max")
    ).reset_index()

    result["idle_minutes"] = (
        result["idle_end"] - result["idle_start"]
    ).dt.total_seconds() / 60

    return result[result["idle_minutes"] > 30]