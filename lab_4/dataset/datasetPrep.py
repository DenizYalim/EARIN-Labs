import pandas as pd

from dataset.config import unclean_data_path, dataset_clean


def clean() -> pd.DataFrame:
    df = pd.read_csv(unclean_data_path)
    df = df.dropna()
    df = df.drop_duplicates()
    df.to_csv(dataset_clean, index=False)  # save cleaned dataset
    return


clean()


def load_clean_dataset():  # from source
    return pd.read_csv(dataset_clean)


def get_as_x_y():
    df = load_clean_dataset()
    y = df["target"]
    X = df.drop(columns=["target"])
    return X, y
