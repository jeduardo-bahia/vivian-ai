import asyncio
from io import BytesIO
import pygame
import edge_tts
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

from .config import ELEVEN_API_KEY, VOICE_ID
from .utils import limpar_texto_para_fala
from .emotions import detectar_emocao, HOTKEYS
from .commands import pressionar_combo, soltar_combo

pygame.init()
pygame.mixer.init()

client = ElevenLabs(api_key=ELEVEN_API_KEY)

async def falar_edge(texto: str):
    texto = limpar_texto_para_fala(texto)

    communicate = edge_tts.Communicate(
        texto,
        voice="pt-BR-FranciscaNeural"
    )

    audio_buffer = BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])

    audio_buffer.seek(0)

    pygame.mixer.music.load(audio_buffer)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.05)

async def falar(texto: str):
    texto_limpo = limpar_texto_para_fala(texto)

    if len(texto_limpo) > 150:
        await falar_edge(texto)
        return

    emocao = detectar_emocao(texto)
    combo = HOTKEYS.get(emocao, HOTKEYS["neutral"])

    try:
        audio_stream = client.text_to_speech.convert(
            voice_id=VOICE_ID,
            model_id="eleven_flash_v2_5",
            text=texto_limpo
        )

        audio_bytes = b"".join(audio_stream)

        pressionar_combo(combo)
        play(audio_bytes)

    finally:
        soltar_combo(combo)
