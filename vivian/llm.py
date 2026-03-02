import asyncio
from .config import MODELO, PERSONALIDADE, MAX_MEM

memoria = []

# ── Motor ──
# "ollama" = local, "groq" = cloud gratuito
_motor = "ollama"
_groq_key = ""  # preenchido via set_groq_key() ou config.py

# Tenta importar GROQ_API_KEY do config se existir
try:
    from .config import GROQ_API_KEY
    _groq_key = GROQ_API_KEY
except ImportError:
    pass

# Modelo Groq padrão (pode ser trocado nas configs)
MODELO_GROQ = "llama-3.1-8b-instant"  # rápido e gratuito

def set_motor(motor: str):
    global _motor
    _motor = motor
    print(f"[LLM] Motor trocado para: {motor}")

def set_groq_key(key: str):
    global _groq_key
    _groq_key = key

def set_modelo_groq(modelo: str):
    global MODELO_GROQ
    MODELO_GROQ = modelo

def limpar_historico():
    global memoria
    memoria = []
    print("[LLM] Histórico limpo.")

async def _perguntar_ollama(mensagens: list) -> str:
    import ollama
    loop = asyncio.get_event_loop()
    resposta = await loop.run_in_executor(
        None,
        lambda: ollama.chat(model=MODELO, messages=mensagens)
    )
    return resposta["message"]["content"].strip()

async def _perguntar_groq(mensagens: list) -> str:
    from groq import Groq
    loop = asyncio.get_event_loop()
    client = Groq(api_key=_groq_key)
    resposta = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            model=MODELO_GROQ,
            messages=mensagens,
            max_tokens=1024,
        )
    )
    return resposta.choices[0].message.content.strip()

async def perguntar_llm(pergunta: str) -> str:
    global memoria
    from vivian.ui.avatar_window import api

    memoria.append({"role": "user", "content": pergunta})
    memoria = memoria[-MAX_MEM:]

    mensagens = [
        {"role": "system", "content": PERSONALIDADE},
        *memoria
    ]

    api.set_thinking(True)
    try:
        if _motor == "groq":
            texto = await _perguntar_groq(mensagens)
        else:
            texto = await _perguntar_ollama(mensagens)
    except Exception as e:
        print(f"[LLM] Erro no motor '{_motor}': {e}")
        # Fallback para Ollama se Groq falhar
        if _motor == "groq":
            print("[LLM] Tentando fallback para Ollama...")
            try:
                texto = await _perguntar_ollama(mensagens)
            except Exception as e2:
                texto = "Desculpe, ocorreu um erro ao processar sua mensagem."
        else:
            texto = "Desculpe, ocorreu um erro ao processar sua mensagem."
    finally:
        api.set_thinking(False)

    memoria.append({"role": "assistant", "content": texto})
    return texto