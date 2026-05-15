from dataset.datasetPrep import get_as_x_y
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np


def linear_regression():
    X, y = get_as_x_y()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Pipeline([("scaler", StandardScaler()), ("lr", LinearRegression())])

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    print("RMSE:", np.sqrt(mean_squared_error(y_test, pred)))


linear_regression()
