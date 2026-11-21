from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request, send_file


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "roadguard_model.pkl"

app = Flask(__name__, static_folder=None)
app.config.update(JSON_SORT_KEYS=False)


def load_model():
    if not MODEL_PATH.exists():
        return None
    data = joblib.load(MODEL_PATH)
    return data["model"], data["encoders"], data["target_encoder"]


model_data = load_model()


@app.route("/")
def home():
    return send_file(BASE_DIR / "index.html")


@app.route("/styles.css")
def styles():
    return send_file(BASE_DIR / "styles.css")


@app.route("/script.js")
def script():
    return send_file(BASE_DIR / "script.js")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "online",
        "model_loaded": model_data is not None,
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    if model_data is None:
        return jsonify({
            "error": "Model is not available. Run demo.py and train .py first."
        }), 503

    model, encoders, target_encoder = model_data
    payload = request.get_json(silent=True) or {}
    aliases = {
        "weather": "weather",
        "road_type": "road",
        "traffic_density": "traffic",
        "time_of_day": "time",
        "road_condition": "condition",
    }

    values = {}
    try:
        for column, key in aliases.items():
            value = payload.get(key)
            if value not in encoders[column].classes_:
                raise ValueError(f"Invalid {key}: {value}")
            values[column] = encoders[column].transform([value])[0]

        speed = float(payload["speed"])
        visibility = float(payload["visibility"])
        if not 0 <= speed <= 200:
            raise ValueError("Speed must be between 0 and 200 km/h")
        if not 0 <= visibility <= 50:
            raise ValueError("Visibility must be between 0 and 50 km")

        row = pd.DataFrame([values])
        row["speed_limit"] = speed
        row["visibility_km"] = visibility
        prediction = model.predict(row)
        result = target_encoder.inverse_transform(prediction)[0]
        probability = None
        if hasattr(model, "predict_proba"):
            probability = round(
                float(model.predict_proba(row).max(axis=1)[0]) * 100,
                1,
            )

        return jsonify({"risk_level": result, "confidence": probability})
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="127.0.0.1", port=5000)