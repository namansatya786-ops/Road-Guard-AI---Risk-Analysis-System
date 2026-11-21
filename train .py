import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

BASE_DIR = Path(__file__).resolve().parent
dataset_path = BASE_DIR / "dataset" / "roadguard_demo_data.csv"
model_dir = BASE_DIR / "model"
model_dir.mkdir(parents=True, exist_ok=True)

if not dataset_path.exists():
    raise FileNotFoundError(
        f"Dataset not found: {dataset_path}. Run demo.py first."
    )

df = pd.read_csv(dataset_path)

categorical = [
    "weather",
    "road_type",
    "traffic_density",
    "time_of_day",
    "road_condition"
]

encoders = {}

for col in categorical:
    encoders[col] = LabelEncoder()
    df[col] = encoders[col].fit_transform(df[col])

target_encoder = LabelEncoder()

df["risk_level"] = target_encoder.fit_transform(
    df["risk_level"]
)

X = df.drop("risk_level", axis=1)
y = df["risk_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)

model.fit(X_train, y_train)

prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print("Model Accuracy:", accuracy)

joblib.dump(
    {
        "model": model,
        "encoders": encoders,
        "target_encoder": target_encoder
    },
    model_dir / "roadguard_model.pkl"
)

print("RoadGuard AI Model Saved Successfully!")