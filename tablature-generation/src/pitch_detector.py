import librosa
import numpy as np

def extract_pitches(audio_path, sr=22050, fmin=82, fmax=1000):
    """
    Extrai frequências fundamentais (pitch) de um áudio.
    Retorna: lista de (tempo, frequência) apenas para frames com pitch válido.
    """
    y, sr = librosa.load(audio_path, sr=sr, mono=True)

    # pyin: f0 array com np.nan quando sem pitch, voiced_flag booleano
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=fmin,
        fmax=fmax,
        sr=sr
    )

    times = librosa.times_like(f0, sr=sr)

    # filtra apenas frames onde 'voiced_flag' é True e freq não é NaN
    pitches = []
    for t, freq, voiced in zip(times, f0, voiced_flag):
        if voiced and freq is not None and not np.isnan(freq) and freq > 0:
            pitches.append((float(t), float(freq)))

    return pitches
