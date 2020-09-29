class Chatbot:
    

    def __init__(self,token):
        self.token = token
        self.conversation = []

    def undestandPhrase(self,phrase):
        print(f"Message received: {phrase}")
        if phrase == 'a':
            return "I undestood"
        elif phrase == 'b':
            return "I not undestood"
        else:
            return "Please, repeat"

from collections import defaultdict

class ChatbotInstance:
    _instance_reference = defaultdict(None)

    @classmethod
    def get(self,token):

        if token not in self._instance_reference:
            self._instance_reference[token] = Chatbot(token = token)

        return self._instance_reference[token]

    @classmethod
    def delete(self,token):
        try:
            del self._instance_reference[token]
            return True
        except:
            return False
    pass