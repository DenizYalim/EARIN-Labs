import pandas as pd
from sklearn.datasets import load_diabetes
from dataset.config import unclean_data_path

data = load_diabetes(as_frame=True)
df = data.frame

print(df.columns.tolist())

df.to_csv(unclean_data_path, index=False)  # download

print(f"Downloaded dataset to {unclean_data_path}")
