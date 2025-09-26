# main.py
from pitch_detector import extract_pitches
from note_mapping import freq_to_tab_position
from tab_renderer import render_tab

def audio_to_tab(audio_path, debug=False):
    """
    Pipeline: áudio -> pitches -> tablatura.
    Retorna string com tablatura.
    """
    pitches = extract_pitches(audio_path)
    if debug:
        print(f"[debug] pitches extraídos (n={len(pitches)}) sample: {pitches[:10]}")

    sequence = []
    for t, freq in pitches:
        note, positions = freq_to_tab_position(freq)
        if note is None or not positions:
            # pula frames inválidos
            continue
        string, fret = positions[0]  # heurística simples: primeira opção
        sequence.append((t, note, string, fret))

    if not sequence:
        return "Nenhuma nota detectada / tablatura vazia."

    return render_tab(sequence)
