import asyncio
import os
import threading
import http.server
import webview

UI_DIR     = os.path.dirname(os.path.abspath(__file__))
VIVIAN_DIR = os.path.dirname(UI_DIR)
HTTP_PORT  = 8765

_loop: asyncio.AbstractEventLoop = None


def _iniciar_servidor():
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None
    os.chdir(VIVIAN_DIR)
    server = http.server.HTTPServer(("127.0.0.1", HTTP_PORT), handler)
    server.serve_forever()


class Api:
    def __init__(self):
        self._window = None
        self._vrm_path = f"http://127.0.0.1:{HTTP_PORT}/assets/vivian1.0.vrm"

    def set_window(self, window):
        self._window = window

    def get_vrm_path(self):
        return self._vrm_path

    def set_engine(self, engine: str):
        """Troca o motor de TTS: 'elevenlabs', 'edge' ou 'hybrid'."""
        from vivian import voice
        voice.set_engine(engine)

    def importar_vrm(self):
        """Importa VRM via tkinter e recarrega o avatar."""
        import shutil
        import threading
        resultado = [None]

        def _abrir():
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            path = filedialog.askopenfilename(
                title="Selecionar modelo VRM",
                filetypes=[("VRM Files", "*.vrm"), ("Todos os arquivos", "*.*")]
            )
            root.destroy()
            resultado[0] = path or None

        t = threading.Thread(target=_abrir)
        t.start()
        t.join(timeout=60)

        src = resultado[0]
        if not src:
            print("[VRM] Nenhum arquivo selecionado.")
            return None

        nome = os.path.basename(src)
        dest = os.path.join(VIVIAN_DIR, 'assets', nome)
        print(f"[VRM] Copiando {src} → {dest}")
        if os.path.normcase(os.path.abspath(src)) != os.path.normcase(os.path.abspath(dest)):
            shutil.copy2(src, dest)
        else:
            print("[VRM] Arquivo já está na pasta assets, pulando cópia.")

        self._vrm_path = f"http://127.0.0.1:{HTTP_PORT}/assets/{nome}"
        print(f"[VRM] Novo path: {self._vrm_path}")
        self._js(f"window.recarregarVRM('{self._vrm_path}')")
        return nome

    def get_automacoes(self):
        from vivian import automations
        return automations.get_todas()

    def salvar_automacao(self, idx: int, nome: str, palavra1: str, palavra2: str, caminho: str, ativo: bool):
        from vivian import automations
        print(f"[Auto] Salvando slot {idx}: nome={nome}, p1={palavra1}, p2={palavra2}, caminho={caminho}, ativo={ativo}")
        automations.atualizar(idx, nome, palavra1, palavra2, caminho, ativo)
        return True

    def selecionar_arquivo_auto(self):
        """Abre diálogo via tkinter — funciona sempre no Windows."""
        import threading
        resultado = [None]

        def _abrir():
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            path = filedialog.askopenfilename(
                title="Selecionar arquivo de automação",
                filetypes=[
                    ("Todos os executáveis", "*.exe;*.bat;*.py;*.cmd"),
                    ("Executável", "*.exe"),
                    ("Batch", "*.bat"),
                    ("Python", "*.py"),
                    ("Todos os arquivos", "*.*"),
                ]
            )
            root.destroy()
            resultado[0] = path or None

        t = threading.Thread(target=_abrir)
        t.start()
        t.join(timeout=60)
        print(f"[Auto] Arquivo selecionado: {resultado[0]}")
        return resultado[0]

    def set_llm_motor(self, motor: str, groq_key: str = ""):
        from vivian import llm
        llm.set_motor(motor)
        if groq_key:
            llm.set_groq_key(groq_key)

    def set_groq_model(self, modelo: str):
        from vivian import llm
        llm.set_modelo_groq(modelo)

    def limpar_memoria(self):
        """Limpa o histórico de mensagens do LLM."""
        from vivian import llm
        llm.limpar_historico()

    def get_gesture_paths(self):
        base = f"http://127.0.0.1:{HTTP_PORT}/assets/gestures"
        return {
            "idle":     f"{base}/dwarf_idle.fbx",
            "thinking": f"{base}/Thinking.fbx",
            "thankful": f"{base}/Thankful.fbx",
        }

    def processar(self, texto: str, voz_ativa: bool = True):
        import asyncio
        from vivian.llm import perguntar_llm
        from vivian.voice import falar
        from vivian.emotions import detectar
        from vivian import automations

        async def _processar():
            # Verifica automações primeiro
            resultado_auto = automations.verificar_e_executar(texto)
            if resultado_auto:
                resposta = f"Certo! Executando {resultado_auto} agora."
                await falar(resposta, voz_ativa)
                return {"resposta": resposta, "emocao": "joy"}

            resposta = await perguntar_llm(texto)
            emocao, gesto = detectar(resposta)
            if gesto:
                self.play_gesture(gesto)
            await falar(resposta, voz_ativa)
            return {"resposta": resposta, "emocao": emocao}

        future = asyncio.run_coroutine_threadsafe(_processar(), _loop)
        return future.result(timeout=120)

    def parar(self):
        """Para o áudio imediatamente e reseta o estado."""
        import pygame
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        self._js("window.stopSpeaking()")

    def toggle_mic(self, ativo: bool):
        from vivian import listener
        if ativo:
            listener.iniciar(self._window)
        else:
            listener.parar()

    def _js(self, code: str):
        if self._window:
            try:
                self._window.evaluate_js(code)
            except Exception:
                pass

    def set_thinking(self, v: bool):
        self._js(f"window.setThinking({'true' if v else 'false'})")

    def play_gesture(self, nome: str):
        self._js(f"window.playGesture('{nome}')")


api = Api()


def criar_janela(loop: asyncio.AbstractEventLoop):
    global _loop
    _loop = loop

    threading.Thread(target=_iniciar_servidor, daemon=True).start()

    # Inicializa automações
    from vivian import automations
    automations.init(VIVIAN_DIR)

    window = webview.create_window(
        "Vivian",
        f"http://127.0.0.1:{HTTP_PORT}/ui/vivian.html",
        js_api=api,
        width=480,
        height=700,
        resizable=True,
        frameless=False,
    )
    api.set_window(window)

    def on_loaded():
        from vivian.voice import set_window
        set_window(window)

    window.events.loaded += on_loaded
    webview.start(debug=False)