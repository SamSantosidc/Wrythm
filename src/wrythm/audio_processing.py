"""
Módulo responsável pelo carregamento e pré-processamento de áudio.
Explora funções do Librosa para normalização, resample e segmentação.
"""

import librosa
import numpy as np


def load_audio(path: str, sr: int = 22050):
    """
    Carrega arquivo de áudio para análise.
    Retorna (y, sr) onde y é o array do sinal e sr a taxa de amostragem.
    """
    y, sr = librosa.load(path, sr=sr, mono=True)
    return y, sr


def normalize_audio(y: np.ndarray):
    """Normaliza o sinal de áudio (amplitude entre -1 e 1)."""
    return librosa.util.normalize(y)


def trim_silence(y: np.ndarray):
    """Remove silêncio inicial/final do áudio."""
    y_trimmed, _ = librosa.effects.trim(y)
    return y_trimmed


def segment_audio(y: np.ndarray, sr: int, segment_duration: float = 5.0):
    """
    Segmenta o áudio em blocos de segment_duration segundos.
    Retorna lista de arrays.
    """
    seg_samples = int(segment_duration * sr)
    return [y[i:i + seg_samples] for i in range(0, len(y), seg_samples)]
