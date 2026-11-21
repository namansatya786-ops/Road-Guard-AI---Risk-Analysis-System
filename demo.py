from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
DATASET_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

n = 5000

weather = np.random.choice(
    ["Clear", "Rain", "Fog", "Cloudy"], n
)

road_type = np.random.choice(
    ["Highway", "Urban", "Rural", "Intersection"], n
)

traffic = np.random.choice(
    ["Low", "Medium", "High"], n
)

time = np.random.choice(
    ["Morning", "Afternoon", "Evening", "Night"], n
)

condition = np.random.choice(
    ["Good", "Wet", "Damaged"], n
)

speed = np.random.choice(
    [30, 40, 50, 60, 80, 100], n
)

visibility = np.random.uniform(1, 15, n)

risk = []

for i in range(n):

    score = 0

    if weather[i] == "Rain":
        score += 2

    if weather[i] == "Fog":
        score += 3

    if traffic[i] == "High":
        score += 2

    if time[i] == "Night":
        score += 2

    if condition[i] == "Damaged":
        score += 3

    if visibility[i] < 3:
        score += 2

    if speed[i] >= 80:
        score += 1

    if score >= 6:
        risk.append("High")

    elif score >= 3:
        risk.append("Medium")

    else:
        risk.append("Low")


df = pd.DataFrame({
    "weather": weather,
    "road_type": road_type,
    "traffic_density": traffic,
    "time_of_day": time,
    "road_condition": condition,
    "speed_limit": speed,
    "visibility_km": visibility,
    "risk_level": risk
})

df.to_csv(DATASET_DIR / "roadguard_demo_data.csv", index=False)

print("Dataset generated successfully!")