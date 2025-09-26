# src/dataset_builder.py
import os, requests, json, numpy as np, soundfile as sf
import librosa
from pathlib import Path
from spotify_setup import sp  # client pessoal (Informações ocultadas na .env)

def safe_filename(s):
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in s)[:200]

def download_preview(url, out_path):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(r.content)
    return out_path

def extract_features(audio_path, sr=22050, n_mfcc=40, rhythmic_bins=16, melodic_segments=16):
    # carrega (librosa lida com mp3).
    y, _sr = librosa.load(audio_path, sr=sr, mono=True, duration=30.0)

    # MFCC  (Características de timbres).
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    mfcc_mean = mfcc.mean(axis=1)          # vetor n_mfcc (vetor que armazena tais características).
    mfcc_var  = mfcc.var(axis=1)

    # BPM / beats (Utilizando o librosa, extraímos o BPM da música).
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    tempo = float(tempo)

    # rhythmic_cell: histogram de onsets dividido em bins ao longo da duração (Visualiza os ataques[momentos de grandes picos] e calcula a o tempo entre eles).
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    duration = len(y) / sr
    rhythmic_hist, _ = np.histogram(onset_times, bins=rhythmic_bins, range=(0, duration))
    rhythmic_cell = rhythmic_hist.astype(int).tolist()

    # melodic_cell: chroma, pega dominante por segmento.
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)  # shape (12, T)
    T = chroma.shape[1]
    seg_len = max(1, T // melodic_segments)
    melodic_cell = []
    for i in range(melodic_segments):
        seg = chroma[:, i*seg_len:(i+1)*seg_len]
        if seg.size == 0:
            melodic_cell.append(int(np.argmax(chroma.mean(axis=1))))
        else:
            melodic_cell.append(int(np.argmax(seg.mean(axis=1))))
    # melodic_cell é lista de ints 0..11

    # key estimate (heurístico simples) (Tom da música/áudio).
    chroma_mean = chroma.mean(axis=1)
    key = int(np.argmax(chroma_mean))  # 0..11

    # Empacota
    features = {
        "mfcc_mean": mfcc_mean.astype(float).tolist(),
        "mfcc_var":  mfcc_var.astype(float).tolist(),
        "bpm": tempo,
        "rhythmic_cell": rhythmic_cell,
        "melodic_cell": melodic_cell,
        "key": key,
        "duration": float(duration)
    }
    return features


def save_features_np(out_features_dir, spotify_id, mfcc_array, chroma_array):
    Path(out_features_dir).mkdir(parents=True, exist_ok=True)
    p = Path(out_features_dir) / f"{spotify_id}_features.npz"
    np.savez_compressed(p, mfcc=mfcc_array, chroma=chroma_array)
    return str(p)


# Coletar metadatas dos aúdios coletados pelo spotify.
def process_track_and_write_metadata(track, genre_tag, previews_root="previews", features_root="features", meta_root="metadata"):
    preview_url = track.get("preview_url")
    if not preview_url:
        return None
    track_id = track["id"]
    fname = safe_filename(f"{track_id}_{track['name']}.mp3")
    out_audio = os.path.join(previews_root, genre_tag, fname)
    download_preview(preview_url, out_audio)

    feat = extract_features(out_audio)
    # opcional: resave arrays (se quiser salvar mfcc completos)
    # path_np = save_features_np(os.path.join(features_root, genre_tag), track_id, mfcc_array, chroma_array)
    metadata = {
        "audio_file": out_audio,
        "spotify_id": track_id,
        "track_name": track["name"],
        "artists": [a["name"] for a in track["artists"]],
        "preview_url": preview_url,
        "sample_rate": 22050,
        "duration": feat["duration"],
        "bpm": feat["bpm"],
        "key": feat["key"],
        "rhythmic_cell": feat["rhythmic_cell"],
        "melodic_cell": feat["melodic_cell"],
        # "features_file": path_np,
        "instrumentation": None,
        "genre_tags": [genre_tag]
    }
    meta_dir = os.path.join(meta_root, genre_tag)
    Path(meta_dir).mkdir(parents=True, exist_ok=True)
    meta_path = os.path.join(meta_dir, f"{track_id}.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    return metadata
