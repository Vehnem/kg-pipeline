###DI Task###
from abc import ABC, abstractmethod

class Task(ABC):
    """
    This abstract class represents a generic data integration task
    """

    def __init__(self, config):
        """
        Constructor for the Task class
        :param name: the name of the task
        :param description: the description of the task
        """
        self.name = config['name']
        self.description = config['description']

    @abstractmethod
    def run(self):
        """
        Abstract method representing the action of running the task.
        Each subclass must provide its own implementation for this method.
        """

