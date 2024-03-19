"""Framework Configuration"""
import yaml
import os
from typing import Dict


class Config:
    """
    Config class
    """

    def __init__(self, config_file="config.yaml"):
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        OPENAI= config.get("openai", None)
        OPENAI_API_KEY = OPENAI.get("api-key", None)
        self.OPENAI_API_KEY = OPENAI_API_KEY if OPENAI_API_KEY else os.environ.get("OPENAI_API_KEY")

        ANTHROPIC = config.get("anthropic", None)
        ANTHROPIC_API_KEY = ANTHROPIC.get("api-key", None)
        self.ANTHROPIC_API_KEY = ANTHROPIC_API_KEY = ANTHROPIC_API_KEY if ANTHROPIC_API_KEY else os.environ.get("ANTHROPIC_API_KEY")

        GCLOUD = config.get("gcloud", None)
        GCLOUD_API_KEY = GCLOUD.get("api-key", None)
        self.GCLOUD_API_KEY = GCLOUD_API_KEY if GCLOUD_API_KEY else os.environ.get("GCLOUD_API_KEY")
        GCLOUD_PROJECT_ID = GCLOUD.get("project-id", None)
        self.GCLOUD_PROJECT_ID = GCLOUD_PROJECT_ID if GCLOUD_PROJECT_ID else os.environ.get("GCLOUD_PROJECT_ID")
        GCLOUD_PROJECT_LOCATION = GCLOUD.get("project-location", None)
        self.GCLOUD_PROJECT_LOCATION = GCLOUD_PROJECT_LOCATION if GCLOUD_PROJECT_LOCATION else os.environ.get("GCLOUD_PROJECT_LOCATION")

        self.SNIPPET_DIR = config.get("directories", None).get("snippets", None)
        self.ONTOLOGY_FILE = config.get("directories", None).get("ontology", None)

        self.config = config

    def bindings(self) -> Dict[str, dict]:
        opt_bindings = self.config.get("bindings", None)
        catalog = {}
        for b in opt_bindings:
            catalog.update({b['id']: b})
        return catalog
    

    def llm_models(self) -> Dict[str, dict]:
        opt_llm_models = self.config.get("llm_models", None)
        catalog = {}
        for b in opt_llm_models:
            catalog.update({b['id']: b})
        return catalog


    def llm_tasks(self) -> Dict[str, dict]:
        opt_llm_tasks = self.config.get("llm_tasks", None)
        catalog = {}
        for b in opt_llm_tasks:
            catalog.update({b['id']: b})
        return catalog
    
    def journal_db_url(self) -> str:
        return self.config.get("journal", None).get("db", None).get("url", None)