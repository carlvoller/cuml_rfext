# cuml_rfext
Extension for cuML's `RandomForestClassifier` and `RandomForestRegressor`.

This library adds support for the `feature_importances_` property to `cuml.ensemble.RandomForestClassifier` and `cuml.ensemble.RandomForestRegressor`.

The primary goal of this library is to allow cuML's RandomForest capabilities to be used with sklearn for Recursive Feature Elimination (RFE).

## Installation
This library requires the Cuda 12 Toolkit to be installed, as well as any Nvidia drivers that cuML would typically need. Cuda 11 and below will not work.
> A PR is more than welcomed for Cuda >12 support!

These library **must** also be installed before installing cuml_rfext:
1. pylibraft-cu12
2. cuml-cu12
> You can install these from https://docs.rapids.ai/install/

```zsh
$ pip install cuml_rfext
```

## How to use
Here is a simple example on how to use this library with sklearn's RFE:
```python
import pandas as pd
from cuml_rfext import RandomForestRegressor
from sklearn.feature_selection import RFE
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

X, y = make_regression(n_features=30, n_samples=100)

X_train, X_test, y_train, y_test = train_test_split(
    X.astype('float32'), y.astype('float32'), test_size=0.2, random_state=42, shuffle=False
)

X_train = pd.DataFrame(X_train)
y_train = pd.Series(y_train)

estimator = RandomForestRegressor(
    n_estimators=1000,
    random_state=42,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features=1.0,
    verbose=0,
    n_streams=10,
    n_bins=100
)

rfe = RFE(estimator=estimator, n_features_to_select=3, step=1)
rfe.fit(X_train, y_train)
selected_features = X_train.columns[rfe.support_].tolist()
print(selected_features)
```

## Documentation
The API for both `RandomForestClassifier` and `RandomForestRegressor` is identical to cuML. This library only extends these classes to add the `feature_importances_` property.

## How it works
When cuML constructs its Decision Trees to form the Random Forest, it calculates a `best_metric_val` which represents the impurity gain from splitting at a specific column. Unfortunately, this `best_metric_val` is not exposed through their Python API, neither do they use it to calculate feature importance.

This library extends the underlying C++ implementation with the `feature_importances_` property, which accesses the underlying Decision Trees and calculates the feature importance of each decision tree using this `best_metric_val`. The importances are then averaged among all decision trees, before returning the relative importance of each feature. This is exposed as a Python List of floats.

## License
Copyright © 2025, Carl Ian Voller. Released under the Apache 2.0 License.