"""
Esse módulo gera tablaturas ASCII simples a partir de eventos de nota detectados.

Estratégia:
- Tenta usar uma transcrição baseada em librosa (piptrack) como fallback.
- Opcional: se "basic_pitch" estiver instalado, o usuário pode integrar um passo de transcrição MIDI
  (função placeholder com tentativa de import).
- Mapeia notas MIDI para cordas/fretes segundo afinações (padrão para guitarra EADGBE).
- Gera uma representação ASCII de tablatura em colunas discretas por time_step.

OBS: Este código é intencionalmente simples e voltado para uso educacional e prototipagem.
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
import librosa
import os
import tempfile

# Afinações (valores MIDI das cordas soltas) - ordem: da corda mais grossa para a mais fina
DEFAULT_TUNINGS = {
    "guitar_standard": {
        "names": ["E", "A", "D", "G", "B", "E"],
        "midi": [40, 45, 50, 55, 59, 64],  # E2, A2, D3, G3, B3, E4
    }
}


def _midi_to_note_name(midi: int) -> str:
    """Converte número MIDI para nome de nota (ex: 64 -> E4)."""
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = (midi // 12) - 1
    name = note_names[midi % 12]
    return f"{name}{octave}"


def transcribe_with_librosa(y: np.ndarray, sr: int, hop_length: int = 512, mag_threshold: float = 1e-6) -> List[Dict]:
    """
    Transcrição simples usando librosa.piptrack.
    Retorna uma lista de eventos: {time, midi, freq}
    Nota: funciona melhor para linhas monofônicas (guitarra solo, voz solista, etc.).
    """
    S = np.abs(librosa.stft(y))
    pitches, magnitudes = librosa.piptrack(S=S, sr=sr, hop_length=hop_length)
    frames = pitches.shape[1]
    times = librosa.frames_to_time(np.arange(frames), sr=sr, hop_length=hop_length)

    events: List[Dict] = []
    last_midi = None
    last_time = None

    for i in range(frames):
        mag_col = magnitudes[:, i]
        idx = mag_col.argmax()
        mag = mag_col[idx]
        pitch = pitches[idx, i]
        if mag < mag_threshold or pitch <= 0:
            last_midi = None
            continue
        midi = int(round(librosa.hz_to_midi(pitch)))

        # compress: se for a mesma nota contígua, ignore (faremos compressão depois)
        events.append({"time": float(times[i]), "midi": int(midi), "freq": float(pitch)})

    # compactar eventos consecutivos com mesmo MIDI em um único evento
    compressed: List[Dict] = []
    if events:
        cur = {"time": events[0]["time"], "midi": events[0]["midi"], "freq": events[0]["freq"], "duration": 0.0}
        prev_t = events[0]["time"]
        for e in events[1:]:
            if e["midi"] == cur["midi"]:
                # estender duração
                cur["duration"] = e["time"] - cur["time"]
            else:
                compressed.append(cur.copy())
                cur = {"time": e["time"], "midi": e["midi"], "freq": e["freq"], "duration": 0.0}
        compressed.append(cur)

    return compressed


def midi_to_string_fret(midi: int, tuning_midi: List[int], max_fret: int = 24) -> Optional[Tuple[int, int]]:
    """
    Dado um número MIDI e uma afinação (lista de midi das cordas), retorna (string_index, fret)
    string_index: 0 = corda mais grossa (low E), increasing to highest string.
    Se nenhuma corda puder reproduzir a nota dentro do range [0, max_fret], retorna None.
    Estratégia: escolher a corda que resulte no menor fret >= 0 e <= max_fret. Em caso de empate, escolhe a corda mais grave.
    """
    candidates = []
    for si, open_m in enumerate(tuning_midi):
        fret = midi - open_m
        if 0 <= fret <= max_fret:
            candidates.append((si, fret))
    if not candidates:
        # tenta aproximar (pode acontecer para notas muito graves/altas)
        # aqui optamos por retornar None para indicar "impraticável" no alcance definido
        return None
    # escolher o candidato com menor fret; se empate, o com menor string index (mais grave)
    candidates.sort(key=lambda x: (x[1], x[0]))
    return candidates[0]


def events_to_tab_events(events: List[Dict], tuning: str = "guitar_standard") -> List[Dict]:
    """
    Converte eventos MIDI em eventos de tablatura: {time, string, fret, note}
    """
    tuning_info = DEFAULT_TUNINGS[tuning]
    tuning_midi = tuning_info["midi"]
    out = []
    for e in events:
        midi = int(e["midi"])
        mapping = midi_to_string_fret(midi, tuning_midi)
        if mapping is None:
            # ignorar notas fora do alcance
            continue
        string_idx, fret = mapping
        out.append({
            "time": e["time"],
            "string": int(string_idx),
            "fret": int(fret),
            "note": _midi_to_note_name(midi)
        })
    return out


def render_ascii_tab(tab_events: List[Dict], duration: float, tuning: str = "guitar_standard", time_step: float = 0.25) -> str:
    """
    Gera uma tablatura ASCII simples com colunas discretas por time_step (em segundos).
    - tab_events: lista de {time, string, fret, note}
    - duration: duração total do áudio em segundos (usado para dimensionar a grade)
    Retorna uma string com a tablatura pronta para salvar/exibir.
    """
    tuning_info = DEFAULT_TUNINGS[tuning]
    string_names = tuning_info["names"]
    n_strings = len(string_names)

    n_cols = max(1, int(np.ceil(duration / time_step)))
    col_width = 3  # largura fixa por coluna (para acomodar até 2 dígitos de fret)

    # iniciar linhas com '-'s
    lines = [["-" * col_width for _ in range(n_cols)] for _ in range(n_strings)]

    for ev in tab_events:
        col = int(ev["time"] // time_step)
        if col >= n_cols:
            continue
        s = ev["string"]
        fret_str = str(ev["fret"])[:col_width].rjust(col_width, " ")
        lines[s][col] = fret_str

    # montar string final: mostrar da corda mais aguda para mais grave (convenção de tablatura)
    out_lines = []
    for si in range(n_strings - 1, -1, -1):
        row = "|" + "".join(lines[si]) + "|"
        header = f"{string_names[si]}|"
        out_lines.append(header + row)

    # adicionar pequeno rodapé com tempo por coluna
    time_header = "   " + "".join([f"{(i * time_step):.2f}".ljust(col_width) for i in range(n_cols)])

    return "\n".join(out_lines) + "\n\n" + time_header


def save_tab_to_file(tab_text: str, out_path: str):
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(tab_text)


# Alta-nível: gerar tablatura a partir de arquivo (reutilizando funções do seu pacote)
def generate_tab_from_audio_path(path: str, time_step: float = 0.25, tuning: str = "guitar_standard") -> Tuple[str, List[Dict]]:
    """
    Pipeline rápido para gerar tablatura (ASCII) a partir de um arquivo de áudio.
    Retorna (tab_text, tab_events).

    Observação: essa função usa a transcrição por librosa como padrão. Para melhores resultados
    com áudio polifônico, considere usar uma ferramenta dedicada (basic_pitch, source separation + transcription, etc.).
    """
    y, sr = librosa.load(path, sr=None, mono=True)
    y = librosa.util.normalize(librosa.effects.trim(y)[0])
    duration = len(y) / sr

    events = transcribe_with_librosa(y, sr)
    tab_events = events_to_tab_events(events, tuning=tuning)
    tab_text = render_ascii_tab(tab_events, duration=duration, tuning=tuning, time_step=time_step)
    return tab_text, tab_events

__all__ = [
    "generate_tab_from_audio_path",
    "save_tab_to_file",
    "render_ascii_tab",
    "events_to_tab_events",
    "transcribe_with_librosa"
]