## Anotações teóricas ##

0.
MIDI (Musical Instrument Digital Interface):
É um padrão técnico que permite a comunicação entre instrumentos musicais eletrônicos, computadores e outros dispositivos.
Permite a troca de informações sobre notas, velocidade, pitch, controle e sincronização entre diferentes equipamentos.
É amplamente utilizado na produção musical, permitindo que músicos controlem e manipulem sons eletronicamente. 

1.
y = vetor NumPy com os valores da forma de onda (amplitudes do som ao longo do tempo)
sr = sample rate (taxa de amostragem, em Hz), ou seja, quantas amostras por segundo

Ex: Se sr = 22050, significa que o áudio foi digitalizado com 22.050 amostras por segundo.

2.
Calcula o vetor de frequências reais associadas ao espectro de Fourier do sinal. -> O espectro de Fourier, também conhecido como transformada de Fourier,
é uma ferramenta matemática que permite decompor um sinal em suas componentes de frequência, revelando as diferentes frequências presentes nesse sinal.

np.fft.rfftfreq(N, d) retorna as frequências que correspondem às amostras de saída da FFT para sinais reais:

N = len(y): número de amostras no sinal

d = 1/sr: intervalo entre amostras (inverso da taxa de amostragem)

Ex: Se len(y) = 44100 e sr = 44100, então temos 1 segundo de som, e as frequências vão de 0 Hz até 22050 Hz (Nyquist).

3.
Aplica a FFT real ao sinal y.

A rfft() é otimizada para sinais reais (como áudio).

O resultado é um vetor de números complexos.

Usamos np.abs() para pegar o módulo (intensidade) de cada frequência.

4.
np.argmax(fft_spectrum) encontra o índice da frequência com maior intensidade (amplitude). -> A FFT (Fast Fourier Transform), ou Transformada Rápida de Fourier,
é um algoritmo que calcula a Transformada Discreta de Fourier (DFT) de uma sequência, ou sua inversa (IDFT).Basicamente,
a FFT transforma um sinal de seu domínio original (geralmente tempo ou espaço) para uma representação no domínio da frequência e vice-versa. 

Esse índice é usado para buscar no vetor frequencies.

Resultado: a frequência dominante no áudio.

Ex: Se o som for um tom puro de 440 Hz, esse será o valor retornado aqui.
