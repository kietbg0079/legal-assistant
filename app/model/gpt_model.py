import os
import asyncio
from openai import OpenAI

from .base_model import BaseLLMModel
from app.config import LLM_CONFIG

class GPTModel(BaseLLMModel):
    def __init__(self, model_init_params={}):
        self.parameters = LLM_CONFIG["openai"]
        self.client = OpenAI(**model_init_params)

    def run(self, 
            messages, 
            config_dict={}):
        
        response = self.client.responses.create(
            input=messages,
            n=1,
            **{**self.parameters, **config_dict}
        )

        return response

    async def run_async(self,
                        messages,
                        config_dict={}):
        pass