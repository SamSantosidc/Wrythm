"""
Pipeline principal do Wrythm.
Carrega um áudio, processa, analisa e gera visualizações.
"""

import os
import numpy as np
from wrythm import audio_processing, music_analysis, utils


def main():
    # Selecionar arquivo via janela
    path = audio_processing.select_file()
    if not path:
        print("Nenhum arquivo selecionado.")
        return


    # Converter para WAV
    path_wav = audio_processing.convert_to_wav(path)
    print(f"Arquivo convertido para WAV: {path_wav}")


    # Carregar e pré-processar
    y, sr = audio_processing.load_audio(path)
    y = audio_processing.trim_silence(y)
    y = audio_processing.normalize_audio(y)


    # Análise musical
    bpm = music_analysis.estimate_bpm(y, sr)
    chroma = music_analysis.extract_chroma(y, sr)
    mfcc = music_analysis.extract_mfcc(y, sr)
    centroid, bandwidth, contrast = music_analysis.extract_spectral_features(y, sr)


    # Resultados no terminal
    print(f"🎵 BPM estimado: {float(np.atleast_1d(bpm)[0]):.2f}")
    print(f"🎵 Centroid espectral médio: {centroid.mean():.2f} Hz")
    print(f"🎵 Bandwidth espectral médio: {bandwidth.mean():.2f} Hz")


    # Visualizações
    utils.plot_waveform(y, sr)
    utils.plot_spectrogram(y, sr)
    utils.plot_chroma(chroma, sr)
    utils.plot_mfcc(mfcc, sr)


if __name__ == "__main__":
    main()
