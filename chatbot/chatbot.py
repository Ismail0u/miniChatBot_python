import streamlit as st
from chatbot_logic import Chatbot
from chatbot_utils import ChatbotUtils
from chatbot_voice import VoiceHelper
import os

# Initialisation
bot = Chatbot()
logger = ChatbotUtils()
voice = VoiceHelper()
log_file = "chatbot_log.txt"

st.set_page_config(page_title="🤖 Chatbot Python", layout="centered")

# 💅 Style CSS pour réduire les tailles
st.markdown("""
    <style>
        .stMarkdown p, .stTextInput > label, .stTextInput input, .stButton button, .stForm, .stChatMessage {
            font-size: 14px !important;
        }
        h1 {
            font-size: 24px !important;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Chatbot Python")
st.markdown("_Pose-moi une question !_")

# 🌐 Options
st.sidebar.header("🛠️ Options")
enable_voice_input = st.sidebar.checkbox("🎤 Activer l'entrée vocale", value=False)
enable_tts = st.sidebar.checkbox("🔊 Activer la lecture vocale", value=True)

# 🔁 Historique
if "history" not in st.session_state:
    st.session_state.history = []

# 🗑️ Réinitialiser la conversation
if st.sidebar.button("🗑️ Réinitialiser"):
    st.session_state.history = []
    if os.path.exists(log_file):
        os.remove(log_file)
    st.rerun()

# 🎤 Parole → Texte (remplit le champ automatiquement)
if enable_voice_input and st.button("🎙️ Parler au lieu d’écrire"):
    user_input = voice.listen()
    st.session_state["input_override"] = user_input  # stocker temporairement dans session

# 💬 Zone de saisie (préremplie si reconnaissance vocale)
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Vous :",
                               value=st.session_state.get("input_override", ""),
                               placeholder="Tape ou parle ta question ici...",
                               key="input")
    submit_button = st.form_submit_button("Envoyer")

# 📩 Traitement de la demande
if submit_button and user_input.strip():
    response = bot.get_response(user_input)

    # Ajout à l'historique
    st.session_state.history.append(("Vous", user_input))  # D'abord la question de l'utilisateur
    st.session_state.history.append(("Bot", response))  # Ensuite la réponse du bot

    # Sauvegarde
    logger.log_message(user_input, response)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"Vous : {user_input}\nBot : {response}\n\n")

    # 🔊 Lecture audio après l'affichage de la réponse
    if enable_tts:
        voice.speak(response)

    # Nettoyage override vocal
    st.session_state["input_override"] = ""

# 💬 Affichage de l’historique (dernier en haut)
for speaker, message in reversed(st.session_state.history):
    if speaker == "Vous":
        with st.chat_message("user"):
            st.markdown(f"🧑 **{speaker}** : {message}")
    else:
        with st.chat_message("assistant"):
            st.markdown(f"🤖 **{speaker}** : {message}")
