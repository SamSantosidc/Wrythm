import librosa
import numpy as np

STANDARD_TUNING = {
    6: 82.41, 5: 110.00, 4: 146.83,
    3: 196.00, 2: 246.94, 1: 329.63
}

def freq_to_tab_position(freq):
    note = librosa.hz_to_note(freq)
    positions = []
    for string, base_freq in STANDARD_TUNING.items():
        fret = round(12 * np.log2(freq / base_freq))
        if 0 <= fret <= 20:
            positions.append((string, fret))
    return note, positions
