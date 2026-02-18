# 🗡️ Vivian AI

Assistente virtual por voz, modular e open-source, com integração a LLM local (Ollama) e síntese de voz híbrida (ElevenLabs + Edge TTS).

Vivian foi projetada para ser direta, objetiva e natural, com personalidade própria e arquitetura organizada para colaboração e evolução contínua.

---

## ✨ Funcionalidades

- 🎤 Reconhecimento de voz (SpeechRecognition)
- 🧠 Integração com LLM local via Ollama
- 🔊 Síntese de voz híbrida:
  - ElevenLabs (respostas curtas e rápidas)
  - Edge TTS (fallback para respostas longas)
- 🎭 Sistema de detecção de emoções
- ⌨️ Acionamento de hotkeys baseadas em emoção
- 🧩 Execução de comandos locais
- 🏗️ Estrutura modular pronta para expansão
- 🔐 Uso de variáveis de ambiente (.env)

---

## 🏛️ Arquitetura do Projeto

<img width="234" height="439" alt="image" src="https://github.com/user-attachments/assets/3386db6d-dadd-4ac2-b4d6-0c43c81f364e" />



Arquitetura organizada para facilitar manutenção, testes e colaboração.

---

## 🚀 Instalação

### 1️⃣ Clone o repositório
git clone https://github.com/jeduardo-bahia/vivian-ai.git
cd vivian-ai


### 2️⃣ Instale as dependências
pip install -r requirements.txt


### 3️⃣ Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

<img width="329" height="50" alt="image" src="https://github.com/user-attachments/assets/a8dca393-5efc-4b28-bd26-b9810b554165" />

---

## ▶️ Execução
python run.py

Vivian iniciará aguardando o wake word.

---

## ⚙️ Requisitos

- Python 3.10+
- Ollama instalado e rodando
- Modelo configurado (ex: llama3.2)
- Microfone configurado
- Conta ElevenLabs com API Key

---

## 🧠 Modelo LLM

Por padrão:
llama3.2:1b

Pode ser alterado em `config.py`.

---

## 🔐 Segurança

- A chave da ElevenLabs NÃO é enviada ao GitHub.
- O arquivo `.env` é ignorado via `.gitignore`.

---

## 🛠️ Contribuição

Contribuições são bem-vindas.

1. Fork o projeto
2. Crie uma branch (`feature/nova-feature`)
3. Commit suas alterações
4. Abra um Pull Request

---

## 📜 Licença

MIT License

---

## 👤 Autor

Criado por Jhonanthan Bahia.

Vivian AI é um projeto experimental de assistente por voz com foco em modularidade, personalidade e integração com LLM local.
