import asyncio
from io import BytesIO

import pygame
import edge_tts
from elevenlabs.client import ElevenLabs

from .config import ELEVEN_API_KEY, VOICE_ID
from .utils import limpar_texto_para_fala

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

client = ElevenLabs(api_key=ELEVEN_API_KEY)

def _js(code: str):
    from vivian.ui.avatar_window import api
    api._js(code)

def set_window(window):
    from vivian.ui.avatar_window import api
    api.set_window(window)

_engine = "hybrid"  # padrão: híbrido

def set_engine(engine: str):
    global _engine
    _engine = engine
    print(f"[Voz] Motor trocado para: {engine}")

async def _tocar_bytes(audio_bytes: bytes, fmt: str = "mp3"):
    buf = BytesIO(audio_bytes)
    buf.name = f"audio.{fmt}"
    _js("window.startSpeaking()")
    try:
        pygame.mixer.music.load(buf)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.05)
    finally:
        _js("window.stopSpeaking()")

async def _falar_edge(texto: str):
    communicate = edge_tts.Communicate(texto, voice="pt-BR-FranciscaNeural")
    buf = BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    await _tocar_bytes(buf.getvalue(), fmt="mp3")

async def _falar_eleven(texto: str):
    loop = asyncio.get_event_loop()
    audio_stream = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id="eleven_flash_v2_5",
        text=texto,
    )
    audio_bytes = await loop.run_in_executor(
        None, lambda: b"".join(audio_stream)
    )
    await _tocar_bytes(audio_bytes, fmt="mp3")

async def falar(texto: str, voz_ativa: bool = True):
    if not voz_ativa:
        return
    texto_limpo = limpar_texto_para_fala(texto)
    if not texto_limpo:
        return

    if _engine == "edge":
        await _falar_edge(texto_limpo)
    elif _engine == "elevenlabs":
        try:
            await _falar_eleven(texto_limpo)
        except Exception as e:
            print(f"[Voz] ElevenLabs falhou ({e}), usando Edge TTS")
            await _falar_edge(texto_limpo)
    else:  # hybrid — padrão
        if len(texto_limpo) > 150:
            await _falar_edge(texto_limpo)
        else:
            try:
                await _falar_eleven(texto_limpo)
            except Exception as e:
                print(f"[Voz] ElevenLabs falhou ({e}), usando Edge TTS")
                await _falar_edge(texto_limpo)