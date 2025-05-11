from app.model import GPTModel
from app.constant import MONGO_DB

from .prompts import assitant_prompt

class LegalAssistant:
    def __init__(self, 
                 user_id, 
                 conversation_id):
        self.llm = GPTModel()
        
        self.conversation_id = conversation_id
        self.messages = self._legal_assistant_initialize(user_id=user_id,
                                                         conversation_id=conversation_id)

    def _legal_assistant_initialize(self,
                                    user_id,
                                    conversation_id):
        if MONGO_DB.query_user_by_id(user_id=user_id) == None:
            raise ValueError("User id isn't existed!")
        
        messages = MONGO_DB.get_messages_from_conversation_id(conversation_id=conversation_id)
        return messages

    async def chat(self,
             message):
        MONGO_DB.add_message(
            self.conversation_id,
            message=message, 
            role="user")
        
        system_prompt = {
            "role": "system",
            "content": assitant_prompt
        }

        self.messages.append({
            "role": "user",
            "content": message
        })

        response = await self.llm.run_async([system_prompt] + self.messages)
        
        MONGO_DB.add_message(
            self.conversation_id,
            message=response.output_text,
            role="assistant"    
        )
        return {"response": response.output_text}
