
from abc import ABC, abstractmethod

from llm4kg_tasks.task import DiTask

class EntityMatcher(DiTask):
    """
    This abstract class represents a generic entity matching task
    """

    @abstractmethod
    def run(self):
        """
        Abstract method representing the action of running the task.
        Each subclass must provide its own implementation for this method.
        """
        pass