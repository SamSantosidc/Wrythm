import librosa

def extract_pitches(audio_path, sr=22050, fmin=82, fmax=1000):
    """
    Extrai frequências fundamentais (pitch) de um áudio.

    Retorna: lista de (tempo, frequência)
    """
    y, sr = librosa.load(audio_path, sr=sr, mono=True)
    f0, voiced_flag, _ = librosa.pyin(
        y,
        fmin=fmin, fmax=fmax,
        sr=sr
    )
    times = librosa.times_like(f0, sr=sr)

    pitches = [(t, p) for t, p in zip(times, f0) if p is not None]
    return pitches
