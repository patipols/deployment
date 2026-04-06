def validate(df):
    return df[
        ((df["lat"].isna()) | ((df["lat"] >= 5) & (df["lat"] <= 21))) &
        ((df["lon"].isna()) | ((df["lon"] >= 97) & (df["lon"] <= 106))) &
        ((df["speed"].isna()) | (df["speed"] >= 0))
    ]