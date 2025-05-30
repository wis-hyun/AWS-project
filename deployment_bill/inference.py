import os
import json
import pickle
import torch
import pandas as pd
from datetime import datetime, timedelta
from model import LSTMModel

def model_fn(model_dir):
    model = LSTMModel()
    model.load_state_dict(torch.load(f"{model_dir}/bill_lstm_model.pt", map_location="cpu"))
    model.eval()
    with open(f"{model_dir}/bill_lstm.pkl", "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

def preprocess_data(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values('timestamp', inplace=True)
    df.set_index('timestamp', inplace=True)
    return df

def input_fn(request_body, request_content_type):
    if request_content_type == "application/json":
        data = json.loads(request_body)
        start_date = pd.to_datetime(data["start_date"])
        end_date = pd.to_datetime(data["end_date"])
        unit_price = data.get("unit_price", 180)

        # 🔥 S3에서 validation 데이터셋 로드
        val_path = 's3://smwu-project-datasets/may-dataset/rtu_ground_truth_may.csv'
        df = pd.read_csv(val_path, storage_options={'anon': False})
        df = preprocess_data(df)

        filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]
        horizon = len(filtered_df)

        if horizon < 1:
            raise ValueError("❌ 선택한 기간에 해당하는 데이터가 없습니다.")

        inputs = filtered_df['activePower'].values.reshape(-1, 1)

        return {
            "inputs": torch.tensor(inputs, dtype=torch.float32),
            "horizon": horizon,
            "unit_price": unit_price,
            "start_date": start_date
        }
    else:
        raise ValueError("Unsupported content type or input format")

def predict_fn(input_data, model_scaler_tuple):
    model, scaler = model_scaler_tuple
    inputs = input_data["inputs"]
    horizon = input_data["horizon"]
    unit_price = input_data["unit_price"]
    start_date = input_data["start_date"]

    input_scaled = scaler.transform(inputs.numpy())
    input_scaled_tensor = torch.tensor(input_scaled, dtype=torch.float32).unsqueeze(0)  # (1, seq_len, 1)

    with torch.no_grad():
        output = model(input_scaled_tensor, n_future=horizon)
    output_np = output.squeeze(0).numpy()

    output_inverse = scaler.inverse_transform(output_np)
    predicted_values = output_inverse.flatten().tolist()
    estimated_bills = [round(v * unit_price, 2) for v in predicted_values]

    timestamps = pd.date_range(start=start_date, periods=horizon, freq='H')

    return {
        "timestamps": timestamps.astype(str).tolist(),
        "predicted_values": predicted_values,
        "estimated_bills": estimated_bills
    }

def output_fn(prediction, content_type):
    if content_type == "application/json":
        return json.dumps({
            "timestamps": prediction["timestamps"],
            "values": [[v] for v in prediction["predicted_values"]],
            "estimated_bills": [[v] for v in prediction["estimated_bills"]]
        })
    else:
        raise ValueError("Unsupported response content type")
