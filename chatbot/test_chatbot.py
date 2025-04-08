import json
import random
import unittest

# Charger le fichier JSON et normaliser les clés
with open("chatbot_responses.json", encoding="utf-8") as f:
    raw_data = json.load(f)

chatbot_data = {key.lower().strip(): value for key, value in raw_data.items()}

# Simuler la fonction de réponse du chatbot
def get_bot_response(user_input):
    normalized_input = user_input.lower().strip()
    return random.choice(chatbot_data.get(normalized_input, ["Je ne comprends pas."]))

class TestChatbot(unittest.TestCase):

    def test_chatbot_responses(self):
        """
        Vérifie que chaque question a une réponse valide dans les réponses attendues.
        """
        for question, expected_responses in chatbot_data.items():
            response = get_bot_response(question)
            self.assertIn(response, expected_responses,
                          f"Réponse incorrecte pour '{question}': {response}")

if __name__ == "__main__":
    unittest.main()
