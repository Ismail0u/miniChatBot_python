from datetime import datetime

class ChatbotUtils:
    def __init__(self, log_file='chat_log.txt'):
        self.log_file = log_file

    def log_message(self, user_input, bot_response):
        """Log l'échange dans un fichier texte."""
        with open(self.log_file, 'a', encoding='utf-8') as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} - Vous : {user_input}\n")
            file.write(f"{timestamp} - Bot : {bot_response}\n\n")
