from llm4kg_tasks import task

class LLM4RML(task.Task):
    """
    This class represents the LLM4RML task
    """

    def __init__(self, config):
        super().__init__(config)

    def run(self):
        """
        Run the LLM4RML task
        """
        print("Running LLM4RML task")