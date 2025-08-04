## Walmart Sales Prediction

### Synchronize the Virtual Environemnt
```bash
uv sync
```

### Activate Virtual Environment
```bash
source .venv/bin/activate
```

### Run Cross Validation
```bash
python3 -m src.mlflow_demo.main.cross_val
```


### Start MLFlow Server
```bash
mlflow server --backend-store-uri sqlite:///data/mlflow.db --default-artifact-root file:$(pwd)/data/mlruns --host 0.0.0.0 --port 5000
```