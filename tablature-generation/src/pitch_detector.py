import librosa
import numpy as np
from scipy.signal import medfilt

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

def smooth_pitches(pitches, kernel_size=5):
    """
    Aplica filtro mediano para suavizar variações rápidas de frequência.
    pitches: lista [(tempo, freq)]
    """
    if not pitches:
        return []

    times, freqs = zip(*pitches)
    freqs = np.array(freqs, dtype=float)

    # kernel_size deve ser ímpar e <= tamanho do array
    if kernel_size > len(freqs):
        kernel_size = len(freqs) if len(freqs) % 2 == 1 else len(freqs) - 1
    if kernel_size < 1:
        return list(zip(times, freqs))

    freqs_filtered = medfilt(freqs, kernel_size=kernel_size)
    return list(zip(times, freqs_filtered))

def group_notes(pitches, time_threshold=0.1):
    """
    Agrupa notas próximas no tempo para evitar repetições excessivas.
    """
    if not pitches:
        return []
    grouped = []
    last_t, last_f = pitches[0]
    grouped.append((last_t, last_f))
    for t, f in pitches[1:]:
        if abs(t - last_t) >= time_threshold:
            grouped.append((t, f))
            last_t, last_f = t, f
    return grouped
