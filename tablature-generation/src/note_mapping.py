import librosa
import numpy as np

# Afinação padrão da guitarra (E2..E4)
STANDARD_TUNING = {
    6: 82.4069,   # E2
    5: 110.0000,  # A2
    4: 146.8324,  # D3
    3: 196.0000,  # G3
    2: 246.9417,  # B3
    1: 329.6276   # E4
}

def freq_to_tab_position(freq, max_fret=20):
    """
    Converte frequência para (nota_str, [(string, fret)]) possíveis.
    Se freq inválida retorna (None, []).
    """
    if freq is None or np.isnan(freq) or freq <= 0:
        return None, []

    note = librosa.hz_to_note(freq)
    positions = []
    for string, base_freq in STANDARD_TUNING.items():
        fret = round(12 * np.log2(freq / base_freq))
        if 0 <= fret <= 20:  # limite típico
            positions.append((string, fret))

    # NOVO: ordenar para favorecer cordas soltas e casas baixas
    positions.sort(key=lambda x: (x[1], x[0]))  
    return note, positions