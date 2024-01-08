# LLM Configs

import yaml

class LLMConfig:
    """
    Load and stores configuration for LLM
    """

    openai_key = ""
    not_used = ""

    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()


    def load_config(self):
        """
        Load the configuration from the config file
        """
        with open(self.config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            self.openai_key = config["openai_key"]
            self.not_used = config["not_used"]