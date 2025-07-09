import requests
import numpy as np

URL = "https://localhost/api/v1/ai/predict?name_persona=Kakek"

# Create synthetic PPG signal
duration_seconds = 60
sampling_rate = 250
n_samples = duration_seconds * sampling_rate

time = np.linspace(0, duration_seconds, n_samples)
heart_rate = 75

ppg_signal = (
    np.sin(2 * np.pi * heart_rate/60 * time) +
    0.3 * np.sin(2 * np.pi * 2 * heart_rate/60 * time) +
    0.1 * np.random.normal(0, 1, n_samples)
)

# Convert NumPy array to list for JSON serialization
data = {
    "ppg_input": {
        "signal": ppg_signal.tolist(),
        "heartbeat": 150,
        "sampling_rate": 250,
    },
    "location": {
        "latitude": -90,
        "longitude": -100
    }
}

header = {
    'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhc2QiLCJleHAiOjE3NTIwNzUwNzQsImlhdCI6MTc1MjA3MzI3NCwidHlwZSI6ImFjY2VzcyJ9.j2LspJM9si9bhFRS1YJqwsYTVMWXRrJDFatJnlBS-_k"
}

# Optional: Bypass SSL warnings for self-signed certs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

res = requests.post(URL, json=data, verify=False, headers=header)  # Set verify=True in production

# Output response
print(res.status_code)
print(res.text)
