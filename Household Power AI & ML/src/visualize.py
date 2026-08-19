"""
visualize.py
------------
Exploratory Data Analysis (EDA) plots for the household power
consumption dataset, plus model evaluation / comparison plots.

Skills demonstrated:
    - Exploratory data analysis with matplotlib & seaborn
    - Correlation analysis
    - Model diagnostic plotting (actual vs predicted, error distribution)
    - Feature importance visualization
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def _save_or_show(fig, filename: str, output_dir: str | None):
    """Helper: save figure to disk if output_dir is given, else show it."""
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, filename)
        fig.savefig(path, bbox_inches="tight", dpi=120)
        print(f"Saved: {path}")
        plt.close(fig)
    else:
        plt.show()


def plot_power_distribution(df: pd.DataFrame, output_dir: str | None = None):
    fig = plt.figure()
    plt.hist(df["Global_active_power"], bins=30)
    plt.title("Power Distribution")
    plt.xlabel("Global Active Power (kW)")
    plt.ylabel("Frequency")
    _save_or_show(fig, "01_power_distribution.png", output_dir)


def plot_power_boxplot(df: pd.DataFrame, output_dir: str | None = None):
    fig = plt.figure()
    plt.boxplot(df["Global_active_power"])
    plt.title("Boxplot Power")
    _save_or_show(fig, "02_power_boxplot.png", output_dir)


def plot_voltage_vs_power(df: pd.DataFrame, output_dir: str | None = None):
    fig = plt.figure()
    plt.scatter(df["Voltage"], df["Global_active_power"], alpha=0.3)
    plt.title("Voltage vs Power")
    plt.xlabel("Voltage")
    plt.ylabel("Global Active Power (kW)")
    _save_or_show(fig, "03_voltage_vs_power.png", output_dir)


def plot_hourly_usage(df: pd.DataFrame, output_dir: str | None = None):
    fig = plt.figure()
    hourly = df.groupby("Hour")["Global_active_power"].mean()
    plt.plot(hourly)
    plt.title("Hourly Usage")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Global Active Power (kW)")
    _save_or_show(fig, "04_hourly_usage.png", output_dir)


def plot_correlation_heatmap(df: pd.DataFrame, output_dir: str | None = None):
    fig = plt.figure(figsize=(9, 7))
    sns.heatmap(df.drop(columns=["Datetime"]).corr(), cmap="coolwarm", annot=False)
    plt.title("Correlation Heatmap")
    _save_or_show(fig, "05_correlation_heatmap.png", output_dir)


def plot_pairplot(df: pd.DataFrame, output_dir: str | None = None, sample_size: int = 500):
    grid = sns.pairplot(
        df[["Global_active_power", "Voltage", "Global_intensity"]].sample(sample_size)
    )
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "06_pairplot.png")
        grid.savefig(path, dpi=120)
        print(f"Saved: {path}")
        plt.close("all")
    else:
        plt.show()


def run_full_eda(df: pd.DataFrame, output_dir: str | None = None):
    """Run every EDA plot in sequence."""
    plot_power_distribution(df, output_dir)
    plot_power_boxplot(df, output_dir)
    plot_voltage_vs_power(df, output_dir)
    plot_hourly_usage(df, output_dir)
    plot_correlation_heatmap(df, output_dir)
    plot_pairplot(df, output_dir)


def plot_actual_vs_predicted(y_test, y_pred, title: str, color: str = "tab:blue",
                              output_dir: str | None = None, filename: str = "actual_vs_predicted.png"):
    fig = plt.figure(figsize=(6, 4))
    plt.scatter(y_test, y_pred, alpha=0.3, color=color)
    plt.plot(
        [y_test.min(), y_test.max()],
        [y_test.min(), y_test.max()],
        color="red",
    )
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title(title)
    _save_or_show(fig, filename, output_dir)


def plot_error_distribution(y_test, y_pred, title: str, color: str = "tab:blue",
                             output_dir: str | None = None, filename: str = "error_distribution.png"):
    errors = y_test.values - y_pred if hasattr(y_test, "values") else np.array(y_test) - y_pred
    fig = plt.figure(figsize=(6, 4))
    plt.hist(errors, bins=30, color=color)
    plt.title(title)
    plt.xlabel("Error")
    plt.ylabel("Frequency")
    _save_or_show(fig, filename, output_dir)


def plot_feature_importance(importances: pd.Series, output_dir: str | None = None):
    fig = plt.figure(figsize=(8, 5))
    importances.sort_values(ascending=False).plot(kind="bar", color="steelblue")
    plt.title("Feature Importance — Random Forest")
    plt.ylabel("Importance Score")
    plt.tight_layout()
    _save_or_show(fig, "feature_importance.png", output_dir)


def plot_peak_usage_hours(test_df: pd.DataFrame, output_dir: str | None = None):
    fig = plt.figure(figsize=(8, 4))
    test_df.groupby("Hour")["Predicted"].mean().plot(kind="bar", color="darkorange")
    plt.title("Average Predicted Power Consumption by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Predicted Global Active Power (kW)")
    plt.tight_layout()
    _save_or_show(fig, "peak_usage_hours.png", output_dir)


def plot_model_comparison(comparison_df: pd.DataFrame, output_dir: str | None = None):
    metrics = ["MAE", "RMSE", "R2 Score"]
    lr_vals = comparison_df.loc[comparison_df["Model"] == "Linear Regression", metrics].values.flatten()
    rf_vals = comparison_df.loc[comparison_df["Model"] == "Random Forest", metrics].values.flatten()

    x = np.arange(len(metrics))
    width = 0.35

    fig = plt.figure(figsize=(8, 5))
    plt.bar(x - width / 2, lr_vals, width, label="Linear Regression", color="steelblue")
    plt.bar(x + width / 2, rf_vals, width, label="Random Forest", color="green")
    plt.xticks(x, metrics)
    plt.ylabel("Score")
    plt.title("Model Comparison — Linear Regression vs Random Forest")
    plt.legend()
    plt.tight_layout()
    _save_or_show(fig, "model_comparison.png", output_dir)


def plot_confusion_matrix(cm, display_labels, output_dir: str | None = None):
    from sklearn.metrics import ConfusionMatrixDisplay

    fig, ax = plt.subplots()
    ConfusionMatrixDisplay(cm, display_labels=display_labels).plot(ax=ax)
    plt.title("Confusion Matrix — KNN Usage Classification")
    _save_or_show(fig, "knn_confusion_matrix.png", output_dir)
