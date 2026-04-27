"""Train churn prediction model and log to MLflow."""
from __future__ import annotations

import argparse
import os
import pickle

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split


def parse_args():
    p = argparse.ArgumentParser("Simple MLflow demo (churn prediction)")
    p.add_argument("--csv", default="data/churn_data.csv", help="Path to CSV")
    p.add_argument("--target", default="churn", help="Target column name")
    p.add_argument(
        "--features",
        default="age,tenure_months,monthly_charges,total_charges,num_support_calls",
        help="Comma-separated feature column names",
    )
    p.add_argument("--experiment", default="Churn-Prediction", help="MLflow experiment name")
    p.add_argument("--run", default="run-4", help="MLflow run name")
    p.add_argument("--n-estimators", type=int, default=100, help="RandomForest n_estimators")
    p.add_argument("--test-size", type=float, default=0.5, help="Test split fraction")
    p.add_argument("--random-state", type=int, default=42, help="Random seed")
    p.add_argument("--model-out", default="models/churn_model.pkl", help="Model output path")
    return p.parse_args()


def main():
    args = parse_args()

    # Set MLflow tracking URI from env or use default
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(args.experiment)

    # Load CSV
    if not os.path.exists(args.csv):
        raise SystemExit(f"CSV not found: {args.csv}")

    df = pd.read_csv(args.csv)

    if args.target not in df.columns:
        raise SystemExit(f"Target column '{args.target}' not found in CSV. Columns: {list(df.columns)}")

    features = [c.strip() for c in args.features.split(",") if c.strip()]
    missing_features = [c for c in features if c not in df.columns]
    if missing_features:
        raise SystemExit(f"Feature columns not found in CSV: {missing_features}")

    # Prepare data
    X = df[features]
    y = df[args.target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.random_state
    )

    # Train and log with MLflow
    with mlflow.start_run(run_name=args.run) as run:
        # Log simple params
        mlflow.log_param("n_estimators", args.n_estimators)
        mlflow.log_param("test_size", args.test_size)
        mlflow.log_param("random_state", args.random_state)
        mlflow.log_param("train_rows", len(X_train))
        mlflow.log_param("test_rows", len(X_test))
        mlflow.log_param("features", ",".join(features))

        # Train model
        model = RandomForestClassifier(
            n_estimators=args.n_estimators,
            random_state=args.random_state,
        )
        model.fit(X_train, y_train)

        # Predict + metrics
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        accuracy = float(accuracy_score(y_test, y_pred))
        auc = float(roc_auc_score(y_test, y_proba))

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("auc", auc)
        mlflow.sklearn.log_model(model, "model")

        model_version = run.info.run_id
        model_info = {
            "model": model,
            "version": model_version,
        }

        out_dir = os.path.dirname(args.model_out)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.model_out, "wb") as f:
            pickle.dump(model_info, f)

        # Log saved pickle as a run artifact
        mlflow.log_artifact(args.model_out, artifact_path="model_files")

    print(f"Accuracy: {accuracy:.4f}")
    print(f"AUC-ROC: {auc:.4f}")
    print(f"Model saved to {args.model_out} with version {model_version}")


if __name__ == "__main__":
    main()
