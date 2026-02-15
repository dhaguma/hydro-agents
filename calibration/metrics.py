# calibration/metrics.py
import numpy as np

def nse(qobs, qsim):
    qobs = np.array(qobs)
    qsim = np.array(qsim)
    denom = np.sum((qobs - qobs.mean())**2)
    num = np.sum((qobs - qsim)**2)
    return 1 - num/denom if denom != 0 else -np.inf

def kge(qobs, qsim):
    qobs = np.array(qobs)
    qsim = np.array(qsim)
    if len(qobs) < 2:
        return -np.inf
    r = np.corrcoef(qobs, qsim)[0,1]
    alpha = qsim.std()/qobs.std() if qobs.std() != 0 else 0
    beta = qsim.mean()/qobs.mean() if qobs.mean() != 0 else 0
    return 1 - np.sqrt((r-1)**2 + (alpha-1)**2 + (beta-1)**2)
