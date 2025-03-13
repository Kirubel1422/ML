from sklearn.datasets import fetch_california_housing
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import QuantileTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from matplotlib import pyplot as plt
from pprint import pprint
import pandas as pd

X,y=fetch_california_housing(return_X_y=True)

# create pipeline
pipe=Pipeline(
    [
        ("scale", QuantileTransformer()),
        ("model", KNeighborsRegressor(n_neighbors=10)),
    ]
)

# model=GridSearchCV(
#     estimator=pipe,
#     param_grid={},
#     cv=3
# )

pipe.fit(X,y)

# pprint(model.best_estimator_)
# exit()
y_pred=pipe.predict(X)
plt.scatter(y_pred, y)
plt.show()