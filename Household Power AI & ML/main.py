"""
main.py
-------
End-to-end runner for the Household Power Consumption ML project.

Usage:
    python main.py --data data/household_power_consumption.txt

This script:
    1. Loads and preprocesses the raw dataset
    2. Runs exploratory data analysis (saves plots to outputs/figures)
    3. Trains Linear Regression and Random Forest regressors to
       predict Global Active Power
    4. Compares the two regression models
    5. Trains a KNN classifier to predict a Low/Medium/High usage class
    6. Saves all figures to outputs/figures/ and trained models to
       outputs/models/
"""

import argparse
import os
import joblib

from src.data_preprocessing import preprocess_pipeline
from src import visualize as viz
from src.train_regression import (
    split_regression_data,
    train_linear_regression,
    train_random_forest,
    get_feature_importance,
    build_comparison_table,
)
from src.train_classification import (
    add_usage_class,
    split_classification_data,
    train_knn,
)


def main(data_path: str, output_dir: str = "outputs", save_models: bool = True):
    figures_dir = os.path.join(output_dir, "figures")
    models_dir = os.path.join(output_dir, "models")
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)

    # ---------- 1. Preprocessing ----------
    print("\n=== Loading & Preprocessing Data ===")
    df = preprocess_pipeline(data_path)
    print(f"\nFinal dataset shape: {df.shape}")

    # ---------- 2. Exploratory Data Analysis ----------
    print("\n=== Running EDA ===")
    viz.run_full_eda(df, output_dir=figures_dir)

    # ---------- 3. Regression: Linear Regression & Random Forest ----------
    print("\n=== Training Regression Models ===")
    X_train, X_test, y_train, y_test = split_regression_data(df)

    lr_result = train_linear_regression(X_train, X_test, y_train, y_test)
    print("\n" + lr_result.summary())
    viz.plot_actual_vs_predicted(
        lr_result.y_test, lr_result.y_pred, "Linear Regression — Prediction Accuracy",
        color="tab:blue", output_dir=figures_dir, filename="07_lr_actual_vs_predicted.png",
    )
    viz.plot_error_distribution(
        lr_result.y_test, lr_result.y_pred, "Linear Regression — Prediction Error Distribution",
        color="tab:blue", output_dir=figures_dir, filename="08_lr_error_distribution.png",
    )

    rf_result = train_random_forest(X_train, X_test, y_train, y_test)
    print("\n" + rf_result.summary())
    viz.plot_actual_vs_predicted(
        rf_result.y_test, rf_result.y_pred, "Random Forest — Prediction Accuracy",
        color="green", output_dir=figures_dir, filename="09_rf_actual_vs_predicted.png",
    )
    viz.plot_error_distribution(
        rf_result.y_test, rf_result.y_pred, "Random Forest — Prediction Error Distribution",
        color="green", output_dir=figures_dir, filename="10_rf_error_distribution.png",
    )

    # ---------- 4. Feature Importance & Peak Usage ----------
    print("\n=== Feature Importance (Random Forest) ===")
    importances = get_feature_importance(rf_result.model, X_train.columns)
    print(importances)
    viz.plot_feature_importance(importances, output_dir=figures_dir)

    test_df = X_test.copy()
    test_df["Actual"] = rf_result.y_test.values
    test_df["Predicted"] = rf_result.y_pred
    viz.plot_peak_usage_hours(test_df, output_dir=figures_dir)

    # ---------- 5. Model Comparison ----------
    print("\n=== Model Comparison ===")
    comparison = build_comparison_table(lr_result, rf_result)
    print(comparison.to_string(index=False))
    viz.plot_model_comparison(comparison, output_dir=figures_dir)

    # ---------- 6. Classification: KNN Usage Class ----------
    print("\n=== Training KNN Usage Classifier ===")
    df_classified = add_usage_class(df)
    Xc_train, Xc_test, yc_train, yc_test = split_classification_data(df_classified)
    knn_result = train_knn(Xc_train, Xc_test, yc_train, yc_test)

    print(f"\nKNN Accuracy: {knn_result.accuracy:.4f}")
    print("\nClassification Report:\n", knn_result.report)
    viz.plot_confusion_matrix(knn_result.confusion_matrix, ["Low", "Medium", "High"], output_dir=figures_dir)

    # ---------- 7. Save Models ----------
    if save_models:
        joblib.dump(lr_result.model, os.path.join(models_dir, "linear_regression.joblib"))
        joblib.dump(rf_result.model, os.path.join(models_dir, "random_forest.joblib"))
        joblib.dump(knn_result.model, os.path.join(models_dir, "knn_classifier.joblib"))
        print(f"\nModels saved to {models_dir}/")

    print("\n=== Pipeline Complete ===")
    print(f"Figures saved to: {figures_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Household Power Consumption ML pipeline")
    parser.add_argument(
        "--data", type=str, default="data/household_power_consumption.txt",
        help="Path to the raw dataset file",
    )
    parser.add_argument(
        "--output", type=str, default="outputs",
        help="Directory to save figures and trained models",
    )
    parser.add_argument(
        "--no-save-models", action="store_true",
        help="Skip saving trained models to disk",
    )
    args = parser.parse_args()

    main(args.data, args.output, save_models=not args.no_save_models)
