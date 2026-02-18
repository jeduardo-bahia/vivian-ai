import re

HOTKEYS = {
    "neutral": "0",
    "joy": "1",
    "angry": "2",
    "sorrow": "3",
    "fun": "4",
    "surprise": "5",
    "negacao": "6",
    "ate": "7",
    "parabens": "8"
}

def detectar_emocao(texto: str) -> str:
    t = texto.lower().strip()

    if "oh!" in t:
        return "surprise"
    if t.endswith("!"):
        return "joy"
    if re.search(r"(tchau|até logo|até mais)", t):
        return "ate"
    if re.search(r"(haha|kkk|engraçado)", t):
        return "fun"
    if re.search(r"(obrigado|excelente|perfeito)", t):
        return "joy"
    if re.search(r"(não|nunca|impossível)", t):
        return "negacao"
    if re.search(r"(triste|lamento|desculpe)", t):
        return "sorrow"
    if re.search(r"(odeio|raiva)", t):
        return "angry"

    return "neutral"
