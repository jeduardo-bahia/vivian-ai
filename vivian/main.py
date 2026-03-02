import asyncio
import threading
from .ui.avatar_window import criar_janela


def iniciar_loop_asyncio(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def main():
    loop = asyncio.new_event_loop()
    threading.Thread(target=iniciar_loop_asyncio, args=(loop,), daemon=True).start()

    criar_janela(loop)

    loop.call_soon_threadsafe(loop.stop)