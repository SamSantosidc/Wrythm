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


