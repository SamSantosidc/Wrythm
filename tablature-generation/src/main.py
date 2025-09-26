from pitch_detector import extract_pitches, smooth_pitches, group_notes
from note_mapping import freq_to_tab_position
from tab_renderer import render_tab

def audio_to_tab(audio_path, debug=False):
    # 1 - Extrair frequências
    pitches = extract_pitches(audio_path)

    # 2 - Suavizar variações rápidas
    pitches = smooth_pitches(pitches, kernel_size=7)

    # 3 - Agrupar por tempo (reduz repetições)
    pitches = group_notes(pitches, time_threshold=0.12)

    sequence = []
    for t, freq in pitches:
        note, positions = freq_to_tab_position(freq)
        if note is None or not positions:
            continue
        string, fret = positions[0]  # heurística: pega a 1ª opção
        sequence.append((t, note, string, fret))

    # 4 - Renderizar tablatura
    tab = render_tab(sequence)

    if debug:
        print(f"[DEBUG] Total de notas processadas: {len(sequence)}")

    return tab
