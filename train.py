"""Train churn prediction model, log to MLflow, and register in Model Registry."""

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
    p = argparse.ArgumentParser("MLflow + Model Registry (churn prediction)")
    p.add_argument("--csv", default="data/churn_data.csv")
    p.add_argument("--target", default="churn")
    p.add_argument(
        "--features",
        default="age,tenure_months,monthly_charges,total_charges,num_support_calls",
    )
    p.add_argument("--experiment", default="Churn-Prediction")
    p.add_argument("--run", default="run-5")
    p.add_argument("--n-estimators", type=int, default=100)
    p.add_argument("--test-size", type=float, default=0.5)
    p.add_argument("--random-state", type=int, default=42)
    p.add_argument("--model-out", default="models/churn_model.pkl")
    return p.parse_args()


def main():
    args = parse_args()

    # 🔥 IMPORTANT: Connect to MLflow server
    mlflow.set_tracking_uri("http://localhost:5000")

    print("Tracking URI:", mlflow.get_tracking_uri())

    # Set experiment
    mlflow.set_experiment(args.experiment)

    # Load data
    if not os.path.exists(args.csv):
        raise SystemExit(f"CSV not found: {args.csv}")

    df = pd.read_csv(args.csv)

    features = [c.strip() for c in args.features.split(",") if c.strip()]
    X = df[features]
    y = df[args.target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.random_state
    )

    # 🔥 Start MLflow run
    with mlflow.start_run(run_name=args.run) as run:

        # Log params
        mlflow.log_param("n_estimators", args.n_estimators)
        mlflow.log_param("test_size", args.test_size)
        mlflow.log_param("random_state", args.random_state)
        mlflow.log_param("features", ",".join(features))

        # Train model
        model = RandomForestClassifier(
            n_estimators=args.n_estimators,
            random_state=args.random_state,
        )
        model.fit(X_train, y_train)

        # Metrics
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("auc", auc)

        # 🔥 CRITICAL: LOG + REGISTER MODEL
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="churn-model"  # 👈 THIS ENABLES REGISTRY
        )

        # Optional: save .pkl (for learning/debug only)
        os.makedirs("models", exist_ok=True)
        with open(args.model_out, "wb") as f:
            pickle.dump(model, f)

        mlflow.log_artifact(args.model_out, artifact_path="model_files")

    print(f"✅ Accuracy: {accuracy:.4f}")
    print(f"✅ AUC-ROC: {auc:.4f}")
    print("✅ Model logged AND registered successfully!")


if __name__ == "__main__":
    main()