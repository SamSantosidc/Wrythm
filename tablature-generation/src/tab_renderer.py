def render_tab(note_sequence):
    """
    Constrói tablatura a partir de uma sequência de (tempo, corda, casa).
    """
    tab_lines = {i: [] for i in range(1, 7)}  # 6 cordas

    for _, string, fret in note_sequence:
        for s in tab_lines:
            tab_lines[s].append(str(fret) if s == string else "-")

    # monta saída como texto
    tab_output = ""
    for s in sorted(tab_lines.keys(), reverse=True):  # da 1ª à 6ª corda
        tab_output += f"{s}|{''.join(tab_lines[s])}\n"
    return tab_output
