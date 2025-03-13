from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, QuantileTransformer
from sklearn.datasets import fetch_california_housing
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

scalers = {
    'min-max': MinMaxScaler(),
    'standard':StandardScaler(),
    'robust':RobustScaler(),
    'quantile-scaler':QuantileTransformer(output_distribution='normal'),
}

model=KNeighborsRegressor()
X, y=fetch_california_housing(return_X_y=True)
for name, scaler in scalers.items():
    X_scaled=scaler.fit_transform(X)
    mean_score=np.mean(cross_val_score(model,X_scaled,y,cv=5))
    print(f'mean-score: {name}={mean_score}')

plt.hist(x=X)
plt.show()