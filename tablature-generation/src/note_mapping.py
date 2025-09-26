import librosa
import numpy as np

# Afinação padrão da guitarra (Mi baixo → Mi agudo)
STANDARD_TUNING = {
    6: 82.41,   # E2
    5: 110.00,  # A2
    4: 146.83,  # D3
    3: 196.00,  # G3
    2: 246.94,  # B3
    1: 329.63   # E4
}

def freq_to_tab_position(freq):
    """
    Converte frequência para (nota, [(corda, casa)]) possíveis.
    """
    note = librosa.hz_to_note(freq)
    positions = []
    for string, base_freq in STANDARD_TUNING.items():
        fret = round(12 * np.log2(freq / base_freq))
        if 0 <= fret <= 20:  # limite de 20 casas
            positions.append((string, fret))
    return note, positions
