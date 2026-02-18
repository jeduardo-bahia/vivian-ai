import os
import subprocess
import pyautogui

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROGRAMAS = {
    "bloco de notas": "notepad.exe",
    "calculadora": "calc.exe",
    "pss": os.path.join(BASE_DIR, "programs", "Sipros.exe"),
}

def pressionar_combo(combo: str):
    for tecla in combo.split("+"):
        pyautogui.keyDown(tecla)

def soltar_combo(combo: str):
    for tecla in combo.split("+")[::-1]:
        pyautogui.keyUp(tecla)

def executar_comando(texto: str) -> bool:
    texto = texto.lower()

    for nome, caminho in PROGRAMAS.items():
        if f"abrir {nome}" in texto:
            subprocess.Popen(caminho)
            return True

    return False
