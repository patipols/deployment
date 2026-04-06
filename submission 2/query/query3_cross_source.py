import numpy as np

def run(df):

    merged = df.merge(df, on="vehicle_id", suffixes=("_a", "_b"))

    merged = merged[
        (merged["source_a"] != merged["source_b"]) &
        (abs((merged["timestamp_a"] - merged["timestamp_b"]).dt.total_seconds()) < 300)
    ]

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        return R * np.arccos(
            np.cos(lat1) * np.cos(lat2) * np.cos(lon2 - lon1) +
            np.sin(lat1) * np.sin(lat2)
        )

    merged["distance_km"] = haversine(
        merged["lat_a"], merged["lon_a"],
        merged["lat_b"], merged["lon_b"]
    )

    return merged[merged["distance_km"] > 1]