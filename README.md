# RoadGuard AI

RoadGuard AI is a full-stack road-risk monitoring dashboard with a Flask API and a trained machine-learning model.

## Features

- Interactive command-center dashboard
- Road-risk heat-map visualization
- Active alerts and AI recommendations
- Low, Medium, and High risk prediction
- JSON REST API and health endpoint
- Responsive styles and accessible controls

## Project Structure

```text
app.py                  Flask application and REST API
demo.py                 Generates demonstration training data
train .py               Trains and saves the risk model
index.html              Dashboard interface
styles.css              Application styles
script.js               Dashboard and API interactions
dataset/                Generated training data
model/                  Serialized machine-learning model
tests/test_app.py       API integration tests
requirements.txt        Python dependencies
```

## Setup

```powershell
python -m pip install -r requirements.txt
python demo.py
python "train .py"
python app.py
```

`app.py` starts the application with Waitress, a production-style WSGI server,
on `http://127.0.0.1:5000`.

After setup, restart the project at any time with:

```powershell
python app.py
```

Alternatively, use the Windows setup/start script:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-project.ps1
```

## API

### Health

`GET /api/health`

### Prediction

`POST /api/predict`

```json
{
  "weather": "Fog",
  "road": "Intersection",
  "traffic": "High",
  "time": "Night",
  "condition": "Damaged",
  "speed": 100,
  "visibility": 1
}
```

Example:

```json
{
  "risk_level": "High",
  "confidence": 100.0
}
```

## Tests

```powershell
python -m unittest discover -s tests -v
```
