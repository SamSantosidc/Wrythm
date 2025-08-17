[🇧🇷 Versão em Português](README.md) | [🌍 English Version](README.en.md)

# 🎵 Wrythm  

O **Wrythm** é um projeto que combina **Inteligência Artificial e Música**, com o objetivo de oferecer uma nova forma de estudar e compreender a arte musical.  
Diferente de soluções que apenas geram tablaturas automáticas, o Wrythm busca realizar uma análise **técnica, histórica e estilística**, permitindo que músicos não apenas reproduzam, mas também entendam a **essência da música**, seu contexto, e a entonação adequada de cada execução.  

A ferramenta permite:  
- Geração automática de **tablaturas e partituras**.  
- Detecção de **ritmo, estilo e andamento**.  
- Identificação de **características do compositor** e **influências históricas** do período.  
- Explicações didáticas que auxiliam no **letramento musical**, quebrando o paradigma de “só decorar” cifras.  

---

## 🎯 Objetivo  

Promover um aprendizado musical mais profundo, que una **técnica, história e interpretação**, para que músicos e estudantes compreendam o “porquê” por trás da música e não apenas a execução mecânica.  

---

## 📂 Pipeline do Projeto  

1. **Entrada de Áudio**  
   - Upload de arquivos **MP3, MP4 ou links do YouTube**.  
   - Gravação em tempo real via microfone.  

2. **Pré-processamento**  
   - Normalização e limpeza do áudio.  
   - Segmentação em trechos significativos.  

3. **Extração de Features**  
   - Acordes  
   - Tempo (BPM)  
   - Estrutura harmônica  
   - Padrões rítmicos  

4. **Análise Avançada com IA** *(em desenvolvimento)*  
   - Determinação do **estilo musical**.  
   - Reconhecimento de **características composicionais**.  
   - Identificação de **influências históricas** do período.  
   - Sugestão de **interpretação/entonação** adequada.  

5. **Geração de Saída**  
   - **Tablaturas e partituras** automáticas.  
   - Visualização do ritmo e andamento.  
   - Explicações didáticas e exemplos musicais.  

---

## 📊 Funcionalidades  

- Geração de tablaturas em tempo real.  
- Conversão de arquivos de áudio em partitura/tab.  
- Reconstrução dos sons com instrumentos digitais.  
- Detecção de ritmo e célula rítmica básica.  
- Retorno ao usuário do estilo, contexto histórico e características do compositor.  
- Reforço educacional: material explicativo junto ao resultado.  

---

## 🛠 Tecnologias Utilizadas  

- **Python**  
- **pydub** – manipulação de áudio  
- **librosa** – análise de frequências e extração de features  
- **tkinter** – interface gráfica  
- **math** – cálculos matemáticos  
- **os** – manipulação de diretórios e arquivos  

---

## ▶️ Como Executar o Projeto  

Clone este repositório:  

```bash
git clone https://github.com/seu-usuario/wrythm.git
cd wrythm
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

Execute o aplicativo:
```bash
python app.py
```

---

🤝 Contribuição

Sinta-se à vontade para abrir issues e enviar pull requests.
O objetivo do Wrythm é unir tecnologia, música e educação para transformar o aprendizado musical. 🎶

---

🔮 Próximos Passos

- Implementar interface gráfica mais moderna.

- Adicionar visualizações interativas (Plotly).

- Aprimorar IA para análise histórica e estilística.

- Suporte a execução em tempo real via microfone.

- Criar material didático integrado (lendo junto com o resultado da música).

---

📌 Conclusão

O Wrythm se diferencia das soluções existentes ao propor uma abordagem de letramento musical: em vez de apenas mostrar o que tocar, busca explicar o porquê por trás da música, seu ritmo, sua história, o estilo do compositor e a interpretação correta.

Essa integração de tecnologia, música e educação abre caminho para uma nova forma de estudar e vivenciar a música.
