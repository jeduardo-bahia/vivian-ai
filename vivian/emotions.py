import re

# Cada regra: (padrão, emoção, gesto_ou_None)
_REGRAS = [
    (r"oh!",                         "surprise", None),
    (r"(tchau|até logo|até mais|adeus|boa noite)", "ate",      "wave"),
    (r"(haha|kkk|engraçado|rsrs)",   "fun",      None),
    (r"(obrigado|obrigada|agradeço|grata|grato|excelente|perfeito)", "joy", "thankful"),
    (r"(não|nunca|impossível)",      "negacao",  None),
    (r"(triste|lamento|desculpe)",   "sorrow",   None),
    (r"(odeio|raiva)",               "angry",    None),
    (r"(incrível|nossa|uau|sério)",  "surprise", None),
    (r"(parabéns|muito bem|ótimo)",  "parabens", None),
]

def detectar(texto: str) -> tuple[str, str | None]:
    """Retorna (emocao, gesto) para o texto dado."""
    t = texto.lower().strip()

    # Exclamação final → alegria (se nenhuma regra mais específica pegar antes)
    for padrao, emocao, gesto in _REGRAS:
        if re.search(padrao, t):
            return emocao, gesto

    if t.endswith("!"):
        return "joy", None

    return "neutral", None

# Retrocompatibilidade — avatar_window ainda chama detectar_emocao em alguns lugares
def detectar_emocao(texto: str) -> str:
    emocao, _ = detectar(texto)
    return emocao