from app.model import GPTModel
from app.db import MongoDB


class LegalAssistant:
    def __init__(self, 
                 user_id, 
                 conversation_id):
        self.db = MongoDB()
        self.llm = LLMModel()()
        self.messages = self.db.get_conversation_history(conversation_id=conversation_id)

    def chatbot(self, state: State):
        return {"messages": [self.llm.invoke(state["messages"])]}
