"""
Módulo responsável pelo carregamento e pré-processamento de áudio.
Explora funções para normalização, resample e segmentação.
"""

import os
import librosa
import numpy as np
from pydub import AudioSegment
from tkinter import Tk, filedialog


def select_file():
    """Abre uma janela para o usuário selecionar um arquivo de áudio."""
    root = Tk()
    root.withdraw()  # não mostrar janela principal
    file_path = filedialog.askopenfilename(
        title="Selecione um arquivo de áudio",
        filetypes=[
            ("Arquivos de áudio", "*.wav *.mp3 *.flac *.ogg *.m4a"),
            ("Todos os arquivos", "*.*")
        ]
    )
    return file_path if file_path else None


def convert_to_wav(path: str, output_dir="converted"):
    """
    Converte qualquer formato de áudio suportado pelo pydub para WAV.
    Retorna o caminho do arquivo convertido.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = os.path.splitext(os.path.basename(path))[0] + ".wav"
    wav_path = os.path.join(output_dir, filename)

    try:
        audio = AudioSegment.from_file(path)
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        raise Exception(f"Erro ao converter {path} para WAV: {e}")


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
