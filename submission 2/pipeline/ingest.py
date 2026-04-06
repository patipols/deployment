import pandas as pd
from parsers.source_a import parse_source_a
from parsers.source_b import parse_source_b
from parsers.source_c import parse_source_c
from utils.validation import validate
from utils.dedup import deduplicate

def run_pipeline():

    print("Starting pipeline...")

    # ---------- Source A ----------
    df_a = pd.concat([
        parse_source_a("../data/source_a_gps_vendor.json"),
        parse_source_a("../data/source_a_gps_vendor_rerun.json")
    ], ignore_index=True)

    print(f"Source A: {len(df_a)} rows")

    # ---------- Toyota ----------
    df_b, df_events, df_ts = parse_source_b(
        "../data/source_b_toyota_0x51.json",
        "../data/source_b_toyota_0x52.json"
    )

    print(f"Toyota Unified: {len(df_b)} rows")
    print(f"Toyota Events: {len(df_events)} rows")
    print(f"Toyota Timeseries: {len(df_ts)} rows")

    # ---------- Source C ----------
    df_c = parse_source_c("../data/source_c_logistics.xlsx")
    print(f"Source C: {len(df_c)} rows")

    # ---------- Validation ----------
    df_a = validate(df_a)
    df_b = validate(df_b)
    df_c = validate(df_c)

    # ---------- Combine ----------
    df_all = pd.concat([df_a, df_b, df_c], ignore_index=True)

    # ---------- Dedup ----------
    df_all = deduplicate(df_all)

    # ---------- FIX schema ----------
    df_all["raw_event_type"] = df_all["raw_event_type"].astype(str)
    df_all["vehicle_id"] = df_all["vehicle_id"].astype(str)
    df_all["source"] = df_all["source"].astype(str)

    # ---------- Save ----------
    import os
    os.makedirs("../output", exist_ok=True)

    df_all.to_parquet("../output/unified.parquet", index=False)
    df_events.to_parquet("../output/toyota_events.parquet", index=False)
    df_ts.to_parquet("../output/toyota_timeseries.parquet", index=False)

    print("Pipeline finished!")


if __name__ == "__main__":
    run_pipeline()