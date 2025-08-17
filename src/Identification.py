import Manipulation
import os

def main():
    caminho_mp3 = Manipulation.select_mp3()

    if caminho_mp3 is None:
        print("Nenhum arquivo selecionado.")
        return

    print(f"Arquivo selecionado: {caminho_mp3}")

    # Define o caminho .wav com base no .mp3
    caminho_wav = os.path.splitext(caminho_mp3)[0] + ".wav"

    try:
        resultado = Manipulation.mp3_to_wav(caminho_mp3, caminho_wav)
        print(f"Arquivo convertido com sucesso: {resultado}")

        dominant_note = Manipulation.dominant_note_from_wav(caminho_wav)
        print(f"A nota dominante no arquivo é: {dominant_note}")

        notesFromWave = Manipulation.notes_from_wave(caminho_wav)
        print(f"As notas tocadas no arquivo são: {notesFromWave}")

        Manipulation.plot_full_oscilloscope(caminho_wav)  #onda

    except FileNotFoundError as e:
        print(f"[ERRO] {e}")
    except Exception as e:
        print(f"[ERRO] Erro inesperado: {e}")

if __name__ == "__main__":
    main()
