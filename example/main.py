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
    # n_jobs=NUM_WORKERS,
    random_state=42,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features=1.0,
    verbose=0,
    n_streams=10,
    n_bins=100
)

rfe = RFE(estimator=estimator, n_features_to_select=3, step = 1)
rfe.fit(X_train, y_train)
selected_features = X_train.columns[rfe.support_].tolist()
print(selected_features)