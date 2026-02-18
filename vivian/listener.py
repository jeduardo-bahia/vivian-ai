import speech_recognition as sr

rec = sr.Recognizer()
rec.energy_threshold = 800
rec.dynamic_energy_threshold = False

def ouvir():
    with sr.Microphone() as src:
        try:
            audio = rec.listen(src, phrase_time_limit=8)
            return rec.recognize_google(audio, language="pt-BR").lower()
        except:
            return ""
