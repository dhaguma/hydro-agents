# pipeline/calibrator.py
import pandas as pd
from pathlib import Path
import argparse
from calibration.spotpy_gr4j import SpotpyGR4J
from calibration.spotpy_hsamiplus import SpotpyHSAMI

def calibrate(catchment_id, model_name, era5_path, qobs_path, repetitions=2000, parallel=True):
    meteo = pd.read_csv(era5_path, parse_dates=["date"])
    qobs = pd.read_csv(qobs_path)["qobs"].values
    if model_name.lower() == "gr4j":
        cal = SpotpyGR4J(meteo, qobs, catchment_id)
    else:
        cal = SpotpyHSAMI(meteo, qobs, catchment_id)
    out = cal.run_dds(repetitions=repetitions, parallel=parallel)
    print(f"Calibration finished -> {out}")
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--catchment", required=True)
    parser.add_argument("--model", required=True, choices=["gr4j","hsami","hsamiplus","hasmi"])
    parser.add_argument("--era5", required=True)
    parser.add_argument("--qobs", required=True)
    parser.add_argument("--reps", type=int, default=2000)
    parser.add_argument("--no-parallel", action="store_true")
    args = parser.parse_args()
    calibrate(args.catchment, args.model, args.era5, args.qobs, repetitions=args.reps, parallel=not args.no_parallel)
