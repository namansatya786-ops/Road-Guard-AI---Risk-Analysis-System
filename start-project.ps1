$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

python -m pip install -r requirements.txt

if (-not (Test-Path "dataset\roadguard_demo_data.csv")) {
    python demo.py
}

if (-not (Test-Path "model\roadguard_model.pkl")) {
    python "train .py"
}

python app.py
