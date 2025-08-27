"""
Pipeline principal do Wrythm.
Carrega um áudio, processa, analisa e gera visualizações.
Agora com menu para escolher análise ou geração de tablatura.
"""

import os
import numpy as np
from wrythm import audio_processing, music_analysis, utils, tab_generator


def run_analysis(path):
    """Executa a análise musical e mostra resultados/plots."""
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


def run_tab_generator(path):
    """Gera tablatura ASCII a partir do áudio e salva em arquivo (se o usuário quiser)."""
    tab_text, tab_events = tab_generator.generate_tab_from_audio_path(path, time_step=0.25)

    # Perguntar se deseja salvar
    choice = input("Deseja salvar a tablatura em arquivo? (s/n): ").strip().lower()
    if choice == "s":
        out_file = "saida/tab_output.txt"
        tab_generator.save_tab_to_file(tab_text, out_file)
        print(f"✅ Tablatura salva em {out_file}")
    else:
        print("❌ Tablatura não salva.")

    # Sempre mostrar no terminal
    print("\n=== Tablatura Gerada ===")
    print(tab_text)


def main():
    # Selecionar arquivo via janela
    path = audio_processing.select_file()
    if not path:
        print("Nenhum arquivo selecionado.")
        return

    # Converter para WAV (mantém cópia no formato certo)
    path_wav = audio_processing.convert_to_wav(path)
    print(f"Arquivo convertido para WAV: {path_wav}")

    # Menu simples
    while True:
        print("\n=== Menu Wrythm ===")
        print("1 - Análise musical (BPM, espectro, MFCC, cromagrama, etc.)")
        print("2 - Gerar tablatura automática (ASCII)")
        print("3 - Ambos (análise + tablatura)")
        print("0 - Sair")
        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            run_analysis(path_wav)
        elif choice == "2":
            run_tab_generator(path_wav)
        elif choice == "3":
            run_analysis(path_wav)
            run_tab_generator(path_wav)
        elif choice == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
