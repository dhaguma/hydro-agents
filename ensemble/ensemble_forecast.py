# ensemble/ensemble_forecast.py
import numpy as np
import pandas as pd
import json
from pathlib import Path
from models.gr4j_model import GR4JModel
from models.hsamiplus_model import HSAMIPModel
from multiprocessing import Pool, cpu_count

def sample_parameters(base_params, n_samples, perturbation=0.1):
    """
    Sample parameter sets around base_params using log-normal or normal perturbation.
    perturbation: relative std dev (e.g., 0.1 = 10%)
    """
    samples = []
    keys = list(base_params.keys())
    base_vals = np.array([base_params[k] for k in keys], dtype=float)
    for _ in range(n_samples):
        noise = np.random.normal(0, perturbation, size=base_vals.shape)
        vals = base_vals * (1 + noise)
        samp = {k: float(v) for k, v in zip(keys, vals)}
        samples.append(samp)
    return samples

def run_member(args):
    model_name, params, meteo_df = args
    if model_name.lower() == "gr4j":
        model = GR4JModel(params)
    else:
        model = HSAMIPModel(params)
    qsim = model.simulate(meteo_df)
    return qsim

def ensemble_forecast(catchment_id, model_name, params_path, era5_path, n_members=100, perturbation=0.1, out_dir="data/outputs/forecasts"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    meteo = pd.read_csv(era5_path, parse_dates=["date"])
    base_params = json.loads(Path(params_path).read_text())
    samples = sample_parameters(base_params, n_members, perturbation=perturbation)
    args = [(model_name, s, meteo) for s in samples]
    cores = min(cpu_count(), n_members)
    with Pool(cores) as p:
        results = p.map(run_member, args)
    # results: list of qsim arrays
    qsim_matrix = np.vstack(results)  # shape (n_members, n_timesteps)
    df = pd.DataFrame({
        "date": meteo["date"]
    })
    df["qsim_median"] = np.median(qsim_matrix, axis=0)
    df["qsim_p10"] = np.percentile(qsim_matrix, 10, axis=0)
    df["qsim_p90"] = np.percentile(qsim_matrix, 90, axis=0)
    out = Path(out_dir) / f"{catchment_id}_{model_name}_ensemble.csv"
    df.to_csv(out, index=False)
    return out
