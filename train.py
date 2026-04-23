"""Train churn prediction model"""
import pandas as pd
import pickle
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

# Load data
df = pd.read_csv('data/churn_data.csv')

# Features and target
features = ['age', 'tenure_months', 'monthly_charges', 'total_charges', 'num_support_calls']
X = df[features]
y = df['churn']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

print(f"Accuracy: {accuracy:.4f}")
print(f"AUC-ROC: {auc:.4f}")

# MLflow tracking
mlflow.set_tracking_uri("http://localhost:8080")
experiment_name = "Churn-Prediction"
mlflow.set_experiment(experiment_name)

with mlflow.start_run():
    mlflow.log_params({
        "n_estimators": 100,
        "random_state": 42
    })
    mlflow.log_metrics({
        "accuracy": accuracy,
        "auc": auc
    })
    mlflow.sklearn.log_model(model, "model")

    # Save model with version info in pickle
    model_version = mlflow.active_run().info.run_id
    model_info = {
        "model": model,
        "version": model_version
    }
    with open('models/churn_model.pkl', 'wb') as f:
        pickle.dump(model_info, f)

print(f"Model saved to models/churn_model.pkl with version {model_version}")
