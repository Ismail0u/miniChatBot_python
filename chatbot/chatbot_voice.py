import io
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import shutil

class VoiceHelper:
    def __init__(self):
        self.recognizer = sr.Recognizer()

        # Vérifie si ffmpeg est installé pour éviter des erreurs à l'exécution
        if not shutil.which("ffmpeg"):
            print("⚠️ ffmpeg n'est pas installé ou introuvable dans le PATH.")
            print("➡️ Télécharge-le depuis https://ffmpeg.org/download.html et ajoute-le au PATH.")

    def listen(self):
        """Écoute la voix de l'utilisateur et la convertit en texte"""
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
            except Exception as e:
                return f"Erreur inattendue : {e}"

    def speak(self, text):
        """Convertit un texte en parole et le lit à haute voix"""
        try:
            # Génère un MP3 à partir du texte
            tts = gTTS(text=text, lang='fr')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)

            # Joue le fichier audio depuis la mémoire
            audio = AudioSegment.from_file(fp, format="mp3")
            play(audio)

        except Exception as e:
            print(f"❌ Erreur dans la lecture vocale : {e}")
