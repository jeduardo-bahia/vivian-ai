import asyncio
from .listener import ouvir
from .voice import falar
from .llm import perguntar_llm
from .commands import executar_comando
from .config import WAKE_WORDS, SAIR

async def main():
    em_conversa = False

    print("=" * 40)
    print("Vivian pronta para o comando.")
    print("=" * 40)

    while True:
        texto = await asyncio.to_thread(ouvir)

        if not texto:
            continue

        print(f"Ouvi: {texto}")

        ativou = any(w in texto for w in WAKE_WORDS)

        if ativou or em_conversa:

            if any(s in texto for s in SAIR):
                await falar("Como desejar. Até logo.")
                break

            pergunta = texto
            for w in WAKE_WORDS:
                pergunta = pergunta.replace(w, "")
            pergunta = pergunta.strip()

            if executar_comando(pergunta):
                await falar("Pronto.")
                em_conversa = True
                continue

            if not pergunta:
                await falar("Sim, estou ouvindo.")
                em_conversa = True
                continue

            resposta = perguntar_llm(pergunta)
            print(f"Vivian: {resposta}")
            await falar(resposta)
            em_conversa = True
