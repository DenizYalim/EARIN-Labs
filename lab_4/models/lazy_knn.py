from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

from dataset.datasetPrep import get_as_x_y

K_LIST = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41]


def knn(k_value):
    X, y = get_as_x_y()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    params = {
        "n_neighbors": [k_value],
        "weights": ["uniform"],
        "metric": ["euclidean", "manhattan"],
    }

    grid = GridSearchCV(KNeighborsRegressor(), params, cv=4, scoring="neg_root_mean_squared_error")
    grid.fit(X_train, y_train)

    pred = grid.predict(X_test)

    # sqrt( (1/n) * Σ(y_true - y_pred)^2 )
    print(f"k:{k_value}; RMSE:", np.sqrt(mean_squared_error(y_test, pred)))  # Root mean square deviation


X, y = get_as_x_y()
print(f"size: {len(X)}")
for k in K_LIST:
    knn(k)
