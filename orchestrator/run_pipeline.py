# orchestrator/run_pipeline.py
import subprocess
from pathlib import Path
import argparse

def run_command(cmd):
    print(f"Running: {cmd}")
    subprocess.check_call(cmd, shell=True)

def run_full(catchment, model, start, end, reps=2000, parallel=True, ensemble=False, members=100):
    Path("data/processed/era5").mkdir(parents=True, exist_ok=True)
    Path("data/processed/streamflow").mkdir(parents=True, exist_ok=True)
    # 1. ERA5
    run_command(f"python pipeline/era5_processor.py --catchment {catchment} --start {start} --end {end}")
    era5_path = f"data/processed/era5/{catchment}.csv"
    # 2. Streamflow
    run_command(f"python pipeline/streamflow_processor.py --catchment {catchment}")
    qobs_path = f"data/processed/streamflow/{catchment}.csv"
    # 3. Calibration
    parallel_flag = "" if parallel else "--no-parallel"
    run_command(f"python pipeline/calibrator.py --catchment {catchment} --model {model} --era5 {era5_path} --qobs {qobs_path} --reps {reps} {parallel_flag}")
    params_path = f"data/outputs/parameters/{catchment}_{model}_params.json"
    # 4. Forecast
    ensemble_flag = "--ensemble" if ensemble else ""
    run_command(f"python pipeline/forecaster.py --catchment {catchment} --model {model} --params {params_path} --era5 {era5_path} {ensemble_flag} --members {members}")
    print("Pipeline completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--catchment", required=True)
    parser.add_argument("--model", required=True, choices=["gr4j","hsami","hsamiplus","hasmi"])
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--reps", type=int, default=2000)
    parser.add_argument("--no-parallel", action="store_true")
    parser.add_argument("--ensemble", action="store_true")
    parser.add_argument("--members", type=int, default=100)
    args = parser.parse_args()
    run_full(args.catchment, args.model, args.start, args.end, reps=args.reps, parallel=not args.no_parallel, ensemble=args.ensemble, members=args.members)
