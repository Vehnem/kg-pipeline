"""Abstract LLM Client."""

import openai
from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    This abstract class represents a generic electronic device.
    """

    @abstractmethod
    def send(self):
        """
        Abstract method representing the action of turning on the device.
        Each subclass must provide its own implementation for this method.
        """
        pass


class OpenAIClient(LLMClient):
    """
    OpenAI Client Implementation
    """

    def send(self)->str:
        return ""
    

class HttpClient(LLMClient):
    
    def send(self)->str:
        return ""
        