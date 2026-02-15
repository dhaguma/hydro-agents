# pipeline/parameter_updater.py
from pipeline.calibrator import calibrate

def update_parameters(catchment_id, model_name, era5_path, qobs_path, repetitions=1000, parallel=True):
    # Re-run DDS on recent data; lower repetitions for periodic updates
    out = calibrate(catchment_id, model_name, era5_path, qobs_path, repetitions=repetitions, parallel=parallel)
    return out

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--catchment", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--era5", required=True)
    parser.add_argument("--qobs", required=True)
    parser.add_argument("--reps", type=int, default=1000)
    parser.add_argument("--no-parallel", action="store_true")
    args = parser.parse_args()
    update_parameters(args.catchment, args.model, args.era5, args.qobs, repetitions=args.reps, parallel=not args.no_parallel)
