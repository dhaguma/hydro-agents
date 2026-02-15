# pipeline/streamflow_processor.py
import pandas as pd
from pathlib import Path
import argparse

def process_streamflow(catchment_id, out_dir="data/processed/streamflow"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    # Placeholder: replace with real observed data ingestion
    dates = pd.date_range("1990-01-01", "2020-12-31", freq='D')
    df = pd.DataFrame({"date": dates, "qobs": 5.0})
    out = Path(out_dir) / f"{catchment_id}.csv"
    df.to_csv(out, index=False)
    print(f"Streamflow processed -> {out}")
    return out

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--catchment", required=True)
    args = parser.parse_args()
    process_streamflow(args.catchment)
