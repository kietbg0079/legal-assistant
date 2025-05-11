import os
import asyncio
import functools
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
            **{**self.parameters, **config_dict}
        )

        return response.choices[0].message.content

    async def run_async(self,
                        messages,
                        config_dict={}):
        
        final_params = {**self.parameters, 
                        **config_dict}
        sync_api_call = functools.partial(
            self.client.responses.create, 
            input=messages,                          
            **final_params  
        )
        response = await asyncio.to_thread(sync_api_call)
        return response