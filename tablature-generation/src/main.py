from pitch_detector import extract_pitches
from note_mapping import freq_to_tab_position
from tab_renderer import render_tab

def audio_to_tab(audio_path):
    """
    Pipeline: áudio -> pitches -> tablatura
    """
    pitches = extract_pitches(audio_path)
    sequence = []
    for t, freq in pitches:
        note, positions = freq_to_tab_position(freq)
        if positions:
            string, fret = positions[0]  # heurística simples: pega a 1ª opção
            sequence.append((t, string, fret))
    return render_tab(sequence)


if __name__ == "__main__":
    audio_path = "../data/raw/teste.wav"  # troque pelo seu arquivo
    tab = audio_to_tab(audio_path)
    print(tab)
