###DI Task###
from abc import ABC, abstractmethod
from dataclasses import dataclass

class DiTask(ABC):
    """
    This abstract class represents a generic data integration task
    """

    @abstractmethod
    def run(self):
        """
        Abstract method representing the action of running the task.
        Each subclass must provide its own implementation for this method.
        """

@dataclass
class Task(ABC):
    """
    This abstract class represents a generic task
    """
    config: dict


    def __init__(self, config):
        self.config = config
        if 'name' not in self.config:
            raise Exception('Task name is missing')
        if 'type' not in self.config:
            raise Exception('Task type is missing')
        if 'input' not in self.config:
            raise Exception('Task input is missing')
        if 'output' not in self.config:
            raise Exception('Task output is missing')


    @abstractmethod
    def run(self):
        """
        Abstract method representing the action of running the task.
        Each subclass must provide its own implementation for this method.
        """
