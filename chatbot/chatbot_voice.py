from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import io

class VoiceHelper:
    def __init__(self):
        self.recognizer = sr.Recognizer()

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
        try:
            # Convertir le texte en MP3 dans la mémoire
            tts = gTTS(text=text, lang='fr')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)

            # Lire le fichier MP3 en mémoire
            audio = AudioSegment.from_file(fp, format="mp3")
            play(audio)
        except Exception as e:
            print(f"Erreur dans la lecture vocale : {e}")
