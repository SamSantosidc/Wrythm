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


def extract_chroma(y, sr):
    """Extrai cromagrama (energia de cada classe de nota ao longo do tempo)."""
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    return chroma

def extract_mfcc(y, sr, n_mfcc=13):
    """Extrai coeficientes cepstrais de Mel (MFCCs)."""
    return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)