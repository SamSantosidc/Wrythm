import os
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import librosa
import math
from tkinter import Tk, filedialog
from pydub import AudioSegment
from scipy.io.wavfile import read


def select_mp3():

    #Abre uma janela para o usuário selecionar um arquivo MP3.
    #Retorna o caminho selecionado, ou None se o usuário cancelar.

    root = Tk()
    root.withdraw()

    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo MP3",
        filetypes=[("Arquivos MP3", "*.mp3")]
    )

    return caminho if caminho else None


def mp3_to_wav(path_mp3, path_wav):

    #Converte um arquivo MP3 em WAV.

    try:
        audio = AudioSegment.from_mp3(path_mp3)
        audio.export(path_wav, format="wav")
        return path_wav
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo MP3 não encontrado: {path_mp3}")
    except Exception as e:
        raise Exception(f"Erro ao converter MP3 para WAV: {e}")

def freq_to_note(freq):

    '''
    Converte uma frequência (Hz) para o nome da nota musical correspondente
    Frequência da nota A4 (Convenção de afinação)
    Índice MIDI
    '''
    
    if freq <= 0:
        raise ValueError("Frequência deve ser maior que zero.")

    A4 = 440.0  
    semitones = 12 * math.log2(freq / A4)
    note_index = int(round(semitones)) + 69  
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F',
             'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_name = notes[note_index % 12]
    octave = (note_index // 12) - 1
    return f"{note_name}{octave}"


def dominant_note_from_wav(path_wav):
    '''
    Analisa um arquivo .wav e retorna a frequência e a nota musical dominante
    '''
    try:
        y, sr = librosa.load(path_wav)
        frequencies = np.fft.rfftfreq(len(y), 1 / sr)
        fft_spectrum = np.abs(np.fft.rfft(y))

        if len(frequencies) == 0 or len(fft_spectrum) == 0:
            raise ValueError("Falha ao calcular espectro de frequência.")

        peak_freq = frequencies[np.argmax(fft_spectrum)]
        note = freq_to_note(peak_freq)

        return peak_freq, note
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {path_wav}")
    except Exception as e:
        raise Exception(f"Erro na análise do áudio: {e}")

def notes_from_wave(path_wav, interval_duration=0.5):
    '''
    Analisa um arquivo .wav e retorna as notas tocadas em múltiplos intervalos.
    interval_duration: duração de cada intervalo em segundos.
    Retorna uma lista de tuplas (tempo_inicial, freq_dominante, nota).
    '''
    try:
        y, sr = librosa.load(path_wav)
        total_duration = librosa.get_duration(y=y, sr=sr)
        interval_samples = int(interval_duration * sr)
        notes = []

        for start in np.arange(0, len(y), interval_samples):
            end = int(min(start + interval_samples, len(y)))
            segment = y[start:end]
            if len(segment) == 0:
                continue

            frequencies = np.fft.rfftfreq(len(segment), 1 / sr)
            fft_spectrum = np.abs(np.fft.rfft(segment))

            if len(frequencies) == 0 or len(fft_spectrum) == 0:
                continue

            peak_freq = frequencies[np.argmax(fft_spectrum)]
            note = freq_to_note(peak_freq)
            time_start = start / sr
            notes.append((time_start, peak_freq, note))

        return notes
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {path_wav}")
    except Exception as e:
        raise Exception(f"Erro na análise do áudio: {e}")

def plot_full_oscilloscope(path_wav):

    #Exibe a forma de onda (osciloscópio) e espectrograma de um arquivo .wav.

    try:
        y, sr = librosa.load(path_wav, sr=None)

        plt.figure(figsize=(14, 8))

        # Onda
        plt.subplot(2, 1, 1)
        librosa.display.waveshow(y, sr=sr, color='blue')
        plt.title("Forma de Onda (Osciloscópio)")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)

        # Espectrograma 
        plt.subplot(2, 1, 2)
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', cmap='magma')
        plt.title("Espectrograma (Frequência x Tempo)")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Frequência (Hz)")
        plt.colorbar(format="%+2.0f dB")
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {path_wav}")
    except Exception as e:
        raise Exception(f"Erro ao exibir visualização de áudio: {e}")
