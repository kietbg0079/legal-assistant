from abc import ABC, abstractmethod

class BaseLLMModel(ABC):
    @abstractmethod
    def run(self, contents: str, config_dict = {}):
        pass
    
    @abstractmethod
    async def run_async(self, contents: str, config_dict = {}):
        pass