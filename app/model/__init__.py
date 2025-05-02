from abc import ABC, abstractmethod

from .gpt_model import GPTModel

class BaseLLMModel(ABC):
    @abstractmethod
    def run(self, contents: str, config_dict = {}):
        pass
    
    @abstractmethod
    async def run_async(self, contents: str, config_dict = {}):
        pass