# models/hsamiplus_model.py
import numpy as np
from typing import Dict

try:
    # The hydrologie/hsamiplus package exposes hsami2.hsami2
    from hsamiplus.hsami2 import hsami2
except Exception:
    hsami2 = None

class HSAMIPModel:
    def __init__(self, params: Dict = None):
        self.params = params or {}

    def set_parameters(self, params: Dict):
        self.params = params

    def _build_project(self, meteo_df, params):
        """
        Build the 'projet' dictionary expected by hsami2.hsami2()
        This mapping is minimal and should be extended to match the exact hsami2 schema.
        """
        # Convert dates to strings if needed
        dates = meteo_df["date"].dt.strftime("%Y-%m-%d").tolist()
        projet = {
            "Parametres": params,
            "Forcages": {
                "dates": dates,
                "precip": meteo_df["precip"].tolist(),
                "temp": meteo_df.get("temp", [0.0]*len(meteo_df)).tolist(),
                "pet": meteo_df.get("pet", [0.0]*len(meteo_df)).tolist()
            },
            "Simulation": {
                "start": dates[0],
                "end": dates[-1],
                "timestep": "D"
            }
        }
        return projet

    def simulate(self, meteo_df):
        import numpy as _np
        if hsami2 is None:
            return _np.maximum(0, meteo_df["precip"].values * 0.8)
        projet = self._build_project(meteo_df, self.params)
        out = hsami2(projet)  # adapt if hsami2 returns different structure
        # Extract qsim from output; adapt to actual return structure
        if isinstance(out, dict):
            qsim = out.get("qsim") or out.get("Qsim") or out.get("Q_sim")
            if qsim is None:
                # try nested keys
                for v in out.values():
                    if isinstance(v, (list, tuple)):
                        qsim = v
                        break
        else:
            qsim = None
        if qsim is None:
            # fallback
            return _np.maximum(0, meteo_df["precip"].values * 0.8)
        return _np.array(qsim)
