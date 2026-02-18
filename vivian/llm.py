import ollama
from .config import MODELO, PERSONALIDADE, MAX_MEM

memoria = []

def perguntar_llm(pergunta: str) -> str:
    global memoria

    memoria.append({"role": "user", "content": pergunta})
    memoria = memoria[-MAX_MEM:]

    resposta = ollama.chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": PERSONALIDADE},
            *memoria
        ]
    )

    texto = resposta["message"]["content"].strip()
    memoria.append({"role": "assistant", "content": texto})

    return texto
