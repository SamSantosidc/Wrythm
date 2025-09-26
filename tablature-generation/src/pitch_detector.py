import librosa
import numpy as np

def extract_pitches(audio_path, sr=22050):
    y, sr = librosa.load(audio_path, sr=sr, mono=True)
    f0, voiced_flag, _ = librosa.pyin(
        y, fmin=82, fmax=1000, sr=sr
    )
    times = librosa.times_like(f0, sr=sr)
    return [(t, p) for t, p in zip(times, f0) if p is not None]
