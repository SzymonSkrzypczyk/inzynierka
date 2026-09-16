from pathlib import Path
import numpy as np
import pandas as pd
import torch

from timesfm3.torch import TimesFM3Forecaster

KP_DATA = Path(__file__).parent / "data" / "kp.csv"

model = TimesFM3Forecaster.from_pretrained(
    "google/timesfm-3.0-pytorch",
    device="cpu",
)
df = pd.read_csv(KP_DATA, skiprows=2, parse_dates=["time"])

df = (
    df
    .sort_values("time")
    .drop_duplicates("time")
    .reset_index(drop=True)
)

values = df["kp"].values.astype(np.float32)
y, target = values[:-8], values[-8:]

val_pred = model.predict(
    y,
    horizon=8,
    return_quantiles=True
)

print(val_pred.forecast)
print(val_pred.forecast.size)
print(val_pred.__dict__)
print(target)
print(y)
print("error:", np.mean(np.abs(val_pred.forecast - target)))
