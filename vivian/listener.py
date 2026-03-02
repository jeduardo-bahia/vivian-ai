import threading
import speech_recognition as sr

rec = sr.Recognizer()
rec.energy_threshold = 800
rec.dynamic_energy_threshold = False

_thread: threading.Thread = None
_ativo = False
_window = None

def iniciar(window):
    global _ativo, _thread, _window
    if _ativo:
        return
    _window = window
    _ativo = True
    _thread = threading.Thread(target=_loop, daemon=True)
    _thread.start()
    print("[Mic] Microfone ativado.")

def parar():
    global _ativo
    _ativo = False
    print("[Mic] Microfone desativado.")

def _loop():
    global _ativo
    while _ativo:
        texto = _ouvir()
        if texto and _window:
            # Envia o texto como se fosse digitado pelo usuário
            texto_escaped = texto.replace("'", "\\'").replace('"', '\\"')
            try:
                _window.evaluate_js(f"""
                    (function(){{
                        const box = document.getElementById('input-box');
                        if (box && !box.disabled) {{
                            box.value = '{texto_escaped}';
                            doEnviar();
                        }}
                    }})()
                """)
            except Exception as e:
                print(f"[Mic] Erro ao enviar texto: {e}")

def _ouvir() -> str:
    try:
        with sr.Microphone() as src:
            rec.adjust_for_ambient_noise(src, duration=0.3)
            audio = rec.listen(src, phrase_time_limit=8, timeout=5)
            texto = rec.recognize_google(audio, language="pt-BR").lower()
            print(f"[Mic] Reconhecido: {texto}")
            return texto
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"[Mic] Erro: {e}")
        return ""