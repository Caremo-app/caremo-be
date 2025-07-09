import numpy as np
import pickle
import pandas as pd
from scipy import signal
import pywt
from scipy.stats import skew, kurtosis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

ARRHYTHMIA_TYPES = {
    'Asystole': 0,
    'Bradycardia': 1,
    'Tachycardia': 2,
    'Ventricular_Tachycardia': 3,
    'Ventricular_Flutter_Fib': 4
}

class Location(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude (-90 to 90)")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude (-180 to 180)")


class PPGInput(BaseModel):
    signal: List[float]
    heartbeat: int = 90
    sampling_rate: int = 250

class ArrhythmiaPredictor:
    def __init__(self, model_path: str):
        self.model_package = self._load_model(model_path)
        self.model = self.model_package['model']
        self.scaler = self.model_package['scaler']
        self.feature_names = self.model_package['feature_names']
    
    def _load_model(self, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def preprocess(self, ppg_signal, fs):
        ppg_signal = np.array(ppg_signal)
        ppg_signal = ppg_signal[~np.isnan(ppg_signal)]
        if len(ppg_signal) == 0:
            return None
        nyquist = fs / 2
        low, high = 0.5 / nyquist, 8.0 / nyquist
        try:
            b, a = signal.butter(4, [low, high], btype='band')
            ppg_signal = signal.filtfilt(b, a, ppg_signal)
        except:
            pass
        try:
            ppg_signal = signal.detrend(ppg_signal)
        except:
            pass
        mean_val, std_val = np.mean(ppg_signal), np.std(ppg_signal)
        mask = np.abs(ppg_signal - mean_val) < 3 * std_val
        if np.sum(mask) > len(ppg_signal) * 0.5:
            ppg_signal[~mask] = mean_val
        return ppg_signal

    def signal_quality(self, signal_data, fs):
        if signal_data is None or len(signal_data) < fs:
            return 0.0
        score = 0.0
        try:
            b, a = signal.butter(4, 0.1, btype='high')
            noise = signal.filtfilt(b, a, signal_data)
            snr = 10 * np.log10(np.var(signal_data) / (np.var(noise) + 1e-10))
            score += min(snr / 20, 1.0) * 0.3
        except:
            pass
        try:
            peaks, _ = signal.find_peaks(signal_data, distance=fs//4)
            if len(peaks) > 3:
                intervals = np.diff(peaks)
                cv = np.std(intervals) / (np.mean(intervals) + 1e-10)
                score += max(0, 1 - cv) * 0.4
        except:
            pass
        try:
            amp_range = np.ptp(signal_data)
            amp_std = np.std(signal_data)
            if amp_range > 0:
                score += min(amp_std / amp_range, 1.0) * 0.3
        except:
            pass
        return min(score, 1.0)

    def extract_features(self, signal_data, fs):
        features = {}
        if signal_data is None or len(signal_data) == 0:
            return features

        # Time-domain
        features.update({
            'mean': np.mean(signal_data),
            'std': np.std(signal_data),
            'var': np.var(signal_data),
            'min': np.min(signal_data),
            'max': np.max(signal_data),
            'range': np.ptp(signal_data),
            'median': np.median(signal_data),
            'skewness': skew(signal_data),
            'kurtosis': kurtosis(signal_data),
            'energy': np.sum(signal_data ** 2),
            'rms': np.sqrt(np.mean(signal_data ** 2)),
            'zero_crossing_rate': len(np.where(np.diff(np.signbit(signal_data)))[0]) / len(signal_data)
        })

        # Frequency-domain
        freqs, psd = signal.welch(signal_data, fs=fs, nperseg=min(len(signal_data)//4, 1024))
        total_power = np.sum(psd)
        if total_power > 0:
            bands = {
                'vlf_power': (0.003, 0.04),
                'lf_power': (0.04, 0.15),
                'hf_power': (0.15, 0.4),
            }
            for name, (low, high) in bands.items():
                mask = (freqs >= low) & (freqs < high)
                features[name] = np.sum(psd[mask]) / total_power
            features['lf_hf_ratio'] = features['lf_power'] / (features['hf_power'] + 1e-10)
        features['spectral_centroid'] = np.sum(freqs * psd) / (total_power + 1e-10)
        features['spectral_bandwidth'] = np.sqrt(np.sum(((freqs - features['spectral_centroid'])**2) * psd) / (total_power + 1e-10))
        features['dominant_frequency'] = freqs[np.argmax(psd)]

        features['signal_quality'] = self.signal_quality(signal_data, fs)
        return features

    def predict(self, signal_list, fs=250):
        try:
            signal_data = self.preprocess(signal_list, fs)
            if signal_data is None:
                return {'success': False, 'error': 'Signal preprocessing failed'}
            quality = self.signal_quality(signal_data, fs)
            if quality < 0.2:
                return {'success': False, 'error': 'Signal quality too low', 'quality_score': quality}

            features = self.extract_features(signal_data, fs)
            df = pd.DataFrame([features])
            for f in self.feature_names:
                if f not in df.columns:
                    df[f] = 0.0
            df = df[self.feature_names]
            scaled = self.scaler.transform(df)
            prediction = int(self.model.predict(scaled)[0])  # convert np.int64 → int
            proba = self.model.predict_proba(scaled)[0]
            arrhythmia = [k for k, v in ARRHYTHMIA_TYPES.items() if v == prediction][0]
            confidence = float(proba[prediction])  # convert np.float64 → float

            return {
                'success': True,
                'prediction': prediction,
                'arrhythmia_name': arrhythmia,
                'confidence': confidence,
                'quality_score': quality,
                'all_probabilities': {name: float(proba[val]) for name, val in ARRHYTHMIA_TYPES.items()}
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
