def render_tab(note_sequence):
    """
    Recebe lista de (time, note_str, string, fret) e monta uma tablatura textual simples.
    """
    # criar linhas com comprimento igual ao número de eventos
    n = len(note_sequence)
    tab_lines = {i: [] for i in range(1, 7)}

    for _, _, string, fret in note_sequence:
        for s in tab_lines:
            tab_lines[s].append(str(fret) if s == string else "-")

    tab_output = ""
    for s in sorted(tab_lines.keys(), reverse=True):
        tab_output += f"{s}|{''.join(tab_lines[s])}\n"
    return tab_output
