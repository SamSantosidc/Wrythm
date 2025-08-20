"""
Funções utilitárias para visualizações gráficas.
Explora o Librosa.display para diferentes representações.
"""

import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def plot_waveform(y, sr):
    plt.figure(figsize=(12, 3))
    librosa.display.waveshow(y, sr=sr, color="blue")
    plt.title("Forma de Onda")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.show()


def plot_spectrogram(y, sr):
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    plt.figure(figsize=(12, 5))
    librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", cmap="magma")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Espectrograma Logarítmico")
    plt.show()


def plot_chroma(chroma, sr):
    plt.figure(figsize=(12, 4))
    librosa.display.specshow(chroma, y_axis="chroma", x_axis="time", sr=sr, cmap="coolwarm")
    plt.colorbar()
    plt.title("Cromagrama (Notas musicais ao longo do tempo)")
    plt.show()


def plot_mfcc(mfcc, sr):
    plt.figure(figsize=(12, 4))
    librosa.display.specshow(mfcc, x_axis="time", sr=sr)
    plt.colorbar()
    plt.title("MFCCs")
    plt.show()
