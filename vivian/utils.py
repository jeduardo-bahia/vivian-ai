import re

def limpar_texto_para_fala(texto: str) -> str:
    texto = re.sub(r'[*#]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto
