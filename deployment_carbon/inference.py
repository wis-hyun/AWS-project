# inference.py
import torch
import json
import pickle
import pandas as pd
from datetime import datetime, timedelta  # 🔥 이 줄 추가
from model import LSTMModel

def model_fn(model_dir):
    model = LSTMModel()
    model.load_state_dict(torch.load(f"{model_dir}/carbon_model.pt", map_location="cpu"))
    model.eval()
    with open(f"{model_dir}/carbon_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

def input_fn(request_body, request_content_type):
    if request_content_type == "application/json":
        data = json.loads(request_body)

        # Case 1: basic inputs: {"inputs": [[...], [...]]}
        if "inputs" in data:
            inputs = data["inputs"]
            return torch.tensor(inputs, dtype=torch.float32)

        # Case 2: timestamped data: {"data": [{"timestamp": ..., "value": ...}]}
        elif "data" in data:
            df = pd.DataFrame(data["data"])
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df.sort_values("timestamp", inplace=True)
            df.set_index("timestamp", inplace=True)
            values = df["value"].values.reshape(-1, 1)
            return torch.tensor(values, dtype=torch.float32)

    raise ValueError("Unsupported content type or input format")

def predict_fn(input_data, model_scaler_tuple):
    model, scaler = model_scaler_tuple
    input_np = input_data.numpy()
    input_scaled = scaler.transform(input_np)
    input_tensor = torch.tensor(input_scaled, dtype=torch.float32).unsqueeze(0)  # (1, seq_len, 1)
    with torch.no_grad():
        output = model(input_tensor)
    return output.numpy()

def output_fn(prediction, content_type):
    if content_type == "application/json":
        # 시간 생성 (예: 하루 간격으로)
        now = datetime.now()
        timestamps = [(now + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(len(prediction))]
        return json.dumps({
            "timestamps": timestamps,
            "values": prediction.tolist()
        })
    else:
        raise ValueError("Unsupported response content type")