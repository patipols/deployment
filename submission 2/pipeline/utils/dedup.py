def deduplicate(df):
    return df.drop_duplicates(subset=["record_id"])