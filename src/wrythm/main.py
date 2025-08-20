"""
Pipeline principal do Wrythm.
Carrega um áudio, processa, analisa e gera visualizações.
"""

import os
from wrythm import audio_processing, music_analysis, utils


def main():
    # Input
    path = input("Digite o caminho do arquivo de áudio: ").strip()
    if not os.path.exists(path):
        print("Arquivo não encontrado.")
        return

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
    print(f"🎵 BPM estimado: {bpm:.2f}")
    print(f"🎵 Centroid espectral médio: {centroid.mean():.2f} Hz")
    print(f"🎵 Bandwidth espectral médio: {bandwidth.mean():.2f} Hz")

    # Visualizações
    utils.plot_waveform(y, sr)
    utils.plot_spectrogram(y, sr)
    utils.plot_chroma(chroma, sr)
    utils.plot_mfcc(mfcc, sr)


if __name__ == "__main__":
    main()
