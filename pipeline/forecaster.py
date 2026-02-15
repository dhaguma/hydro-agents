# pipeline/forecaster.py
import pandas as pd
import json
from pathlib import Path
import argparse
from models.gr4j_model import GR4JModel
from models.hsamiplus_model import HSAMIPModel
from ensemble.ensemble_forecast import ensemble_forecast

def run_forecast(catchment_id, model_name, params_path, era5_path, ensemble=False, n_members=100, perturbation=0.1):
    Path("data/outputs/forecasts").mkdir(parents=True, exist_ok=True)
    meteo = pd.read_csv(era5_path, parse_dates=["date"])
    params = json.loads(Path(params_path).read_text())
    if ensemble:
        out = ensemble_forecast(catchment_id, model_name, params_path, era5_path, n_members=n_members, perturbation=perturbation)
        print(f"Ensemble forecast saved -> {out}")
        return out
    if model_name.lower() == "gr4j":
        model = GR4JModel(params)
    else:
        model = HSAMIPModel(params)
    qsim = model.simulate(meteo)
    out = Path("data/outputs/forecasts") / f"{catchment_id}_{model_name}_forecast.csv"
    pd.DataFrame({"date": meteo["date"], "qsim": qsim}).to_csv(out, index=False)
    print(f"Forecast saved -> {out}")
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--catchment", required=True)
    parser.add_argument("--model", required=True, choices=["gr4j","hsami","hsamiplus","hasmi"])
    parser.add_argument("--params", required=True)
    parser.add_argument("--era5", required=True)
    parser.add_argument("--ensemble", action="store_true")
    parser.add_argument("--members", type=int, default=100)
    args = parser.parse_args()
    run_forecast(args.catchment, args.model, args.params, args.era5, ensemble=args.ensemble, n_members=args.members)
