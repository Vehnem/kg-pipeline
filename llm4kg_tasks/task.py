###DI Task###
from abc import ABC, abstractmethod

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
