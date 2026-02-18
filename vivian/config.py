import os
from dotenv import load_dotenv

load_dotenv()

# ===== API =====
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

# ===== MODELOS =====
MODELO = "llama3.2:1b"

# ===== WAKE WORDS =====
WAKE_WORDS = ["vivi", "vivia", "vivian", "viviane", "bibia"]
SAIR = ["sair", "desligar", "tchau", "dormir"]

# ===== PERSONALIDADE =====
PERSONALIDADE = (
    "Você é a Vivian. "
    "Seu nome faz referencia a Dama do Lago da mitologia do Rei Arthur. "
    "Seu criador se chama Jhonanthan. "
    "Inteligente, direta e levemente irônica quando faz sentido. "
    "Respostas curtas, naturais e objetivas. "
    "Nunca use emojis. "
    "Finalize sempre suas frases."
)

MAX_MEM = 21
