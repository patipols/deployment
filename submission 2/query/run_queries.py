import pandas as pd
import os

from query1_engine_sessions import run as q1_run
from query2_idle_detection import run as q2_run
from query3_cross_source import run as q3_run


def load_data():
    df = pd.read_parquet("../output/unified.parquet")
    df_events = pd.read_parquet("../output/toyota_events.parquet")
    return df, df_events


def run_queries():

    print("Loading data...")
    df, df_events = load_data()

    print("Running Query 1...")
    q1 = q1_run(df_events)

    print("Running Query 2...")
    q2 = q2_run(df)

    print("Running Query 3...")
    q3 = q3_run(df)

    os.makedirs("../output/query_results", exist_ok=True)

    q1.to_parquet("../output/query_results/query1_engine_sessions.parquet", index=False)
    q2.to_parquet("../output/query_results/query2_idle.parquet", index=False)
    q3.to_parquet("../output/query_results/query3_cross_source.parquet", index=False)

    print("All queries completed!")


if __name__ == "__main__":
    run_queries()