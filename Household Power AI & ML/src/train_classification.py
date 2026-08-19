"""
train_classification.py
------------------------
Trains a K-Nearest Neighbours classifier to categorise each reading
into a usage class (Low / Medium / High), based on electrical
measurements rather than the raw power value itself.

Skills demonstrated:
    - Turning a regression target into a classification target
      (quantile binning) to answer a different business question
    - Classification modelling (KNN)
    - Evaluation with accuracy, classification report, confusion matrix
"""

from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


USAGE_CLASS_LABELS = ["Low", "Medium", "High"]
CLASSIFICATION_FEATURES = [
    "Hour", "Voltage", "Global_intensity",
    "Sub_metering_1", "Sub_metering_2", "Sub_metering_3",
]


@dataclass
class ClassificationResult:
    model_name: str
    model: object
    y_test: pd.Series
    y_pred: object
    accuracy: float
    report: str
    confusion_matrix: object


def add_usage_class(df: pd.DataFrame, target_column: str = "Global_active_power",
                     n_bins: int = 3) -> pd.DataFrame:
    """
    Bin the continuous power target into equal-frequency classes
    (Low / Medium / High) using quantile-based discretization.
    """
    df = df.copy()
    df["usage_class"] = pd.qcut(df[target_column], q=n_bins, labels=USAGE_CLASS_LABELS[:n_bins])
    return df


def split_classification_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """Split features/labels for the usage-class classification task."""
    X = df[CLASSIFICATION_FEATURES]
    y = df["usage_class"]

    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def train_knn(X_train, X_test, y_train, y_test, n_neighbors: int = 5) -> ClassificationResult:
    """Train and evaluate a K-Nearest Neighbours classifier."""
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return ClassificationResult(
        model_name="K-Nearest Neighbours",
        model=model,
        y_test=y_test,
        y_pred=y_pred,
        accuracy=accuracy_score(y_test, y_pred),
        report=classification_report(y_test, y_pred),
        confusion_matrix=confusion_matrix(y_test, y_pred),
    )
