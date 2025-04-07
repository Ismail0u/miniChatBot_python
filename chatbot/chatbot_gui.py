import tkinter as tk
from tkinter import scrolledtext
from chatbot_logic import Chatbot

class ChatbotGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Mini Chatbot")
        self.window.geometry("400x500")
        self.window.configure(bg="#222")

        # Zone d'affichage du chat
        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, bg="#333", fg="white", font=("Arial", 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        # Champ d'entrée utilisateur
        self.entry = tk.Entry(self.window, font=("Arial", 14), bg="#444", fg="white")
        self.entry.pack(padx=10, pady=10, fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        # Boutons
        button_frame = tk.Frame(self.window, bg="#222")
        button_frame.pack(pady=5)
        self.send_button = tk.Button(button_frame, text="Envoyer", command=self.send_message, bg="#007BFF", fg="white")
        self.send_button.pack(side=tk.LEFT, padx=5)
        self.clear_button = tk.Button(button_frame, text="Effacer", command=self.clear_chat, bg="#FF0000", fg="white")
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.chatbot = Chatbot()

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if user_input:
            self.entry.delete(0, tk.END)
            self.display_message(f"Vous : {user_input}", "blue")
            response = self.chatbot.chatbot_response(user_input)
            self.display_message(f"Bot : {response}", "green")

    def display_message(self, message, color):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n", color)
        self.chat_area.tag_config(color, foreground=color)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def clear_chat(self):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def run(self):
        self.window.mainloop()
