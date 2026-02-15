# pipeline/era5_processor.py
import pandas as pd
from pathlib import Path
import argparse

def process_era5(catchment_id, start, end, out_dir="data/processed/era5"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    # Placeholder: replace with real ERA5 download/processing
    dates = pd.date_range(start, end, freq='D')
    df = pd.DataFrame({"date": dates, "precip": 1.0, "temp": 10.0, "pet": 0.5})
    out = Path(out_dir) / f"{catchment_id}.csv"
    df.to_csv(out, index=False)
    print(f"ERA5 processed -> {out}")
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--catchment", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    args = parser.parse_args()
    process_era5(args.catchment, args.start, args.end)
