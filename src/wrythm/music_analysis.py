"""
Módulo de análise musical.
Extração de características da música.
"""

import librosa
import numpy as np


def estimate_bpm(y, sr):
    """Estima o tempo (BPM) da música."""
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo
