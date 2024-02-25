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

class LLM4RML2:

    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
        self.api_key = None
        self.api_connector = None
        self.load_model()
        self.load_api_connector()


    def load_model(self):
        if self.model_name == "gpt-3.5-turbo-instruct":
            self.model = openai.Chat(model=self.model_name)
        else:
            self.model = openai.Completion(model=self.model_name)


    def load_api_connector(self):
        self.api_connector = OpenAIAPIConnector(self.api_key)