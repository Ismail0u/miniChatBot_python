import speech_recognition as sr
import pyttsx3
import threading
import time

class VoiceHelper:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 160)  # Vitesse de la voix
        self.tts_engine.setProperty('volume', 0.9)  # Volume de la voix

    def listen(self):
        with sr.Microphone() as source:
            try:
                print("🎙️ Parle maintenant...")
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language="fr-FR")
                print("📝 Reçu :", text)
                return text
            except sr.UnknownValueError:
                return "Désolé, je n'ai pas compris."
            except sr.RequestError:
                return "Erreur de connexion au service vocal."
            except sr.WaitTimeoutError:
                return "Tu n'as rien dit 😅."

    def speak(self, text):
        # Parler dans un thread séparé
        thread = threading.Thread(target=self._speak_internal, args=(text,))
        thread.start()

    def _speak_internal(self, text):
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Erreur dans la lecture vocale : {e}")
