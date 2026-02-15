# 🌊 Hydro Agents — Modular Hydrologic Modeling Pipeline

Hydro Agents is a fully modular, agent‑driven hydrologic modeling system built around:

- **GR4J** and **HSAMI+** hydrologic models  
- **SPOTPY DDS** calibration with multi‑objective scoring (NSE + KGE)  
- **Daily‑resolution ERA5 and streamflow processing**  
- **Parallel calibration and ensemble forecasting**  
- **VS Code Agents** for orchestration and automation  
- **Reproducible uv‑based Python environment**

This repository provides a complete, extensible workflow for operational hydrologic forecasting, research, and reproducible modeling.

---

## 🚀 Features

### ✔ Real hydrologic models
- **GR4J** (from `amacd31/gr4j`)
- **HSAMI+** (from `hydrologie/hsamiplus`)

### ✔ Calibration with SPOTPY (DDS)
- Multi‑objective: **0.5 × NSE + 0.5 × KGE**
- Parallel execution using all available CPU cores
- Hydrologically meaningful parameter ranges

### ✔ Ensemble forecasting
- Parameter perturbation
- Median, P10, P90 hydrographs
- Multiprocessing for fast simulation

### ✔ Modular pipeline
- ERA5 processing  
- Streamflow ingestion  
- Calibration  
- Forecasting  
- Parameter updating  

### ✔ VS Code Agents
Each pipeline step can be triggered via natural‑language commands inside VS Code.

---

## 📁 Project Structure
hydro-agents/
│
├── data/
│   ├── raw/                # ERA5 + streamflow raw inputs
│   ├── processed/          # Cleaned daily data
│   └── outputs/
│       ├── calibration/    # SPOTPY DDS results
│       ├── forecasts/      # Deterministic + ensemble forecasts
│       └── parameters/     # Calibrated parameter sets
│
├── models/                 # GR4J + HSAMI+ wrappers
├── calibration/            # SPOTPY calibration classes + metrics
├── ensemble/               # Ensemble forecasting utilities
├── pipeline/               # ERA5, streamflow, calibrator, forecaster
├── orchestrator/           # Full pipeline runner
└── .vscode/agents/         # VS Code agent definitions


---

## 🧪 Environment Setup (uv)

This project uses **uv** for fast, reproducible environments.

### 1. Install dependencies

```bash
uv sync --all-extras

This creates a .venv/ folder and installs:
numpy, pandas, scipy
spotpy
GR4J (from GitHub)
HSAMI+ (from GitHub)

2. Activate the environment
source .venv/bin/activate

3. VS Code integration
.vscode/settings.json ensures the correct interpreter is used.

Running the Pipeline
1. Process ERA5 data
python pipeline/era5_processor.py --catchment 04201500 --start 1990-01-01 --end 2020-12-31

2. Process streamflow
python pipeline/streamflow_processor.py --catchment 04201500


3. Calibrate GR4J or HSAMI+
python pipeline/calibrator.py --catchment 04201500 --model gr4j --era5 data/processed/era5/04201500.csv --qobs data/processed/streamflow/04201500.csv --reps 2000

4. Run deterministic forecast
python pipeline/forecaster.py --catchment 04201500 --model gr4j --params data/outputs/parameters/04201500_gr4j_params.json --era5 data/processed/era5/04201500.csv

5. Run ensemble forecast
python pipeline/forecaster.py --catchment 04201500 --model gr4j --params data/outputs/parameters/04201500_gr4j_params.json --era5 data/processed/era5/04201500.csv --ensemble --members 100

6. Full pipeline orchestration
python orchestrator/run_pipeline.py --catchment 04201500 --model gr4j --start 1990-01-01 --end 2020-12-31 --reps 2000 --ensemble --members 100

VS Code Agents
This project includes a set of .vscode/agents/*.md files that allow you to run the entire workflow using natural language inside VS Code Chat.

Examples:
@Hydro Orchestrator run pipeline for catchment 04201500 using gr4j from 1990-01-01 to 2020-12-31

@Calibration Agent calibrate gr4j for 04201500 with 3000 repetitions

ersion Control
A hydrology‑optimized .gitignore is included to avoid committing:

Raw ERA5 data

Raw streamflow data

Large calibration databases

Ensemble forecast files

Python caches and virtual environments

Parameter files and deterministic forecasts are kept under version control.
Roadmap
Add uncertainty quantification (GLUE, DREAM, MCMC)

Add support for sub‑daily models

Add routing modules (Muskingum, kinematic wave)

Add web dashboard for forecast visualization

📜 License
MIT License — feel free to use, modify, and extend.

🙌 Acknowledgements
GR4J model by Perrin et al.
HSAMI+ by the hydrologie/hsamiplus team
SPOTPY by Houska et al.
ERA5 data by ECMWF

Hydro Agents brings these components together into a unified, reproducible workflow.

---

If you want, I can also generate:

- A **Makefile** for running the entire pipeline  
- A **GitHub Actions CI workflow**  
- A **pre‑commit hook** to prevent committing large data files  
- A **CONTRIBUTING.md** for collaborators  

Just tell me what direction you want to take next.

