# 🎵 Wrythm  

[🇧🇷 Versão em Português](README.md) | [🌍 English Version](READMEen.md)

---

## 🇧🇷 Sobre o Projeto  

O **Wrythm** é uma plataforma experimental que integra **Inteligência Artificial e Música**, com foco em **aprendizado musical assistido por tecnologia**.  
O projeto vai além da simples geração automática de partituras ou tablaturas: ele analisa **ritmo, estilo, gênero, contexto histórico e características composicionais**, oferecendo ao estudante uma visão mais completa da obra.  

### 🚀 Funcionalidades Principais  

- 🎼 **Geração automática de tablatura e partitura** a partir de arquivos de áudio ou microfone.  
- ⏱ **Extração rítmica e temporal** (BPM, padrões rítmicos e andamento).  
- 🎶 **Análise harmônica**: acordes, progressões e estrutura da música.  
- 🧑‍🎓 **Ênfase no aprendizado musical**: explicações didáticas sobre estilo, época e autor.  
- 📜 **Identificação de características históricas e estilísticas** relevantes à obra.  

### 📂 Pipeline de Processamento  

1. **Entrada de Áudio** → arquivos (MP3, WAV, MP4) ou microfone em tempo real.  
2. **Pré-processamento** → normalização, redução de ruído, segmentação.  
3. **Extração de Features** → ritmo, acordes, estilo, progressões.  
4. **Análise Avançada (IA)** → gênero, características da época, assinatura composicional.  
5. **Saída** → partitura/tablatura, visualização rítmica e material educativo.  

### 🛠 Tecnologias  

- Python  
- librosa → análise de áudio e features  
- pydub → processamento de áudio  
- tkinter → interface gráfica  
- NumPy / math → cálculos numéricos  
- os → manipulação de arquivos  

### ▶️ Execução  

```bash
git clone https://github.com/seu-usuario/wrythm.git
```

```bash
cd wrythm
```

```bash
pip install -r requirements.txt
```

```bash
python app.py
```

🔮 Roadmap

1. Interface gráfica modernizada.

2. Visualizações interativas (Plotly).

3. IA expandida para análise histórica e estilística.

4. Suporte em tempo real via microfone.

5. Material didático integrado.

🤝 Contribuição

Contribuições são bem-vindas!
Abra issues ou envie PRs para colaborar.
O objetivo do Wrythm é unir tecnologia, música e educação em um só ambiente.
