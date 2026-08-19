"""
train_regression.py
--------------------
Trains and evaluates regression models that predict Global Active
Power (kW) from household electrical readings and time features.

Models:
    1. Linear Regression   - simple, interpretable baseline
    2. Random Forest       - non-linear ensemble model, generally
                              more accurate and used for feature
                              importance analysis

Skills demonstrated:
    - Train/test splitting
    - Regression modelling (linear & ensemble)
    - Model evaluation with MAE, RMSE, R2
    - Feature importance interpretation
    - Structuring reusable, testable ML training functions
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


@dataclass
class RegressionResult:
    """Container for a trained regression model and its evaluation metrics."""
    model_name: str
    model: object
    y_test: pd.Series
    y_pred: np.ndarray
    mae: float
    rmse: float
    r2: float

    def summary(self) -> str:
        return (
            f"----- {self.model_name} Results -----\n"
            f"MAE  : {self.mae:.4f}\n"
            f"RMSE : {self.rmse:.4f}\n"
            f"R2   : {self.r2:.4f}"
        )


def split_regression_data(df: pd.DataFrame, target_column: str = "Global_active_power",
                           test_size: float = 0.2, random_state: int = 42):
    """
    Split the dataframe into train/test sets for regression.

    Drops the Datetime column (not a numeric model feature) and the
    target column from X.
    """
    X = df.drop([target_column, "Datetime"], axis=1)
    y = df[target_column]

    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def train_linear_regression(X_train, X_test, y_train, y_test) -> RegressionResult:
    """Train a Linear Regression baseline model."""
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return RegressionResult(
        model_name="Linear Regression",
        model=model,
        y_test=y_test,
        y_pred=y_pred,
        mae=mean_absolute_error(y_test, y_pred),
        rmse=np.sqrt(mean_squared_error(y_test, y_pred)),
        r2=r2_score(y_test, y_pred),
    )


def train_random_forest(X_train, X_test, y_train, y_test,
                         sample_frac: float = 0.2,
                         n_estimators: int = 50,
                         max_depth: int = 15,
                         random_state: int = 42) -> RegressionResult:
    """
    Train a Random Forest Regressor.

    A fraction of the training data is sampled before fitting to keep
    training time reasonable on the ~2 million row dataset, while
    n_jobs=-1 parallelizes across all available CPU cores.
    """
    X_train_sample = X_train.sample(frac=sample_frac, random_state=random_state)
    y_train_sample = y_train.loc[X_train_sample.index]

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        n_jobs=-1,
        random_state=random_state,
    )
    model.fit(X_train_sample, y_train_sample)
    y_pred = model.predict(X_test)

    return RegressionResult(
        model_name="Random Forest",
        model=model,
        y_test=y_test,
        y_pred=y_pred,
        mae=mean_absolute_error(y_test, y_pred),
        rmse=np.sqrt(mean_squared_error(y_test, y_pred)),
        r2=r2_score(y_test, y_pred),
    )


def get_feature_importance(model: RandomForestRegressor, feature_names) -> pd.Series:
    """Return feature importances sorted from most to least important."""
    importances = pd.Series(model.feature_importances_, index=feature_names)
    return importances.sort_values(ascending=False)


def build_comparison_table(lr_result: RegressionResult, rf_result: RegressionResult) -> pd.DataFrame:
    """Build a side-by-side comparison table of both regression models."""
    return pd.DataFrame({
        "Model": [lr_result.model_name, rf_result.model_name],
        "MAE": [lr_result.mae, rf_result.mae],
        "RMSE": [lr_result.rmse, rf_result.rmse],
        "R2 Score": [lr_result.r2, rf_result.r2],
    })
