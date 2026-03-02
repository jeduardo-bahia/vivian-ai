import os
import json

_CFG_FILE = None

_automacoes = [
    {"nome": "", "palavras": ["", ""], "caminho": "", "ativo": False},
    {"nome": "", "palavras": ["", ""], "caminho": "", "ativo": False},
    {"nome": "", "palavras": ["", ""], "caminho": "", "ativo": False},
    {"nome": "", "palavras": ["", ""], "caminho": "", "ativo": False},
    {"nome": "", "palavras": ["", ""], "caminho": "", "ativo": False},
]

def init(vivian_dir: str):
    global _CFG_FILE
    _CFG_FILE = os.path.join(vivian_dir, "automations.json")
    carregar()

def carregar():
    global _automacoes
    if not _CFG_FILE or not os.path.exists(_CFG_FILE):
        return
    try:
        with open(_CFG_FILE, encoding="utf-8") as f:
            dados = json.load(f)
        for i, slot in enumerate(dados):
            if i < len(_automacoes):
                _automacoes[i] = slot
        ativos = [a for a in _automacoes if a.get("ativo") and a.get("caminho")]
        print(f"[Auto] Carregadas {len(ativos)} automação(ões) ativa(s).")
        for a in ativos:
            print(f"[Auto]   '{a['palavras']}' → {a['caminho']}")
    except Exception as e:
        print(f"[Auto] Erro ao carregar: {e}")

def salvar():
    if not _CFG_FILE:
        print("[Auto] ERRO: _CFG_FILE não definido!")
        return
    try:
        with open(_CFG_FILE, "w", encoding="utf-8") as f:
            json.dump(_automacoes, f, ensure_ascii=False, indent=2)
        print(f"[Auto] Salvo em {_CFG_FILE}")
    except Exception as e:
        print(f"[Auto] Erro ao salvar: {e}")

def get_todas() -> list:
    return _automacoes

def atualizar(idx: int, nome: str, palavra1: str, palavra2: str, caminho: str, ativo: bool):
    global _automacoes
    if 0 <= idx < len(_automacoes):
        _automacoes[idx] = {
            "nome": nome.strip(),
            "palavras": [palavra1.strip().lower(), palavra2.strip().lower()],
            "caminho": caminho.strip(),
            "ativo": bool(ativo),
        }
        print(f"[Auto] Slot {idx} atualizado: {_automacoes[idx]}")
        salvar()

def verificar_e_executar(texto: str):
    t = texto.lower().strip()
    print(f"[Auto] Verificando texto: '{t}'")
    ativos = [a for a in _automacoes if a.get("ativo") and a.get("caminho")]
    print(f"[Auto] {len(ativos)} slot(s) ativo(s)")
    for auto in ativos:
        p1 = auto["palavras"][0] if len(auto["palavras"]) > 0 else ""
        p2 = auto["palavras"][1] if len(auto["palavras"]) > 1 else ""
        print(f"[Auto] Testando p1='{p1}' ({p1 in t}) p2='{p2}' ({p2 in t})")
        if p1 and p2 and p1 in t and p2 in t:
            return executar(auto)
    return None

def executar(auto: dict):
    caminho = auto["caminho"]
    nome    = auto["nome"] or caminho
    print(f"[Auto] Executando: {caminho}")
    try:
        if not os.path.exists(caminho):
            print(f"[Auto] ERRO: Arquivo não encontrado: {caminho}")
            return f"Não encontrei o arquivo de '{nome}'."
        os.startfile(caminho)
        print(f"[Auto] ✓ Executado com sucesso")
        return nome
    except Exception as e:
        print(f"[Auto] ERRO ao executar: {e}")
        return None