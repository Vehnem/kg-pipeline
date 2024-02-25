import yaml
import os
from typing import Dict

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

OPENAI= config.get("openai", None)
OPENAI_API_KEY = OPENAI.get("api-key", None)

ANTHROPIC = config.get("anthropic", None)
ANTHROPIC_API_KEY = ANTHROPIC.get("api-key", None)

class Config:
    OPENAI_API_KEY = OPENAI_API_KEY if OPENAI_API_KEY else os.environ.get("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = ANTHROPIC_API_KEY if ANTHROPIC_API_KEY else os.environ.get("ANTHROPIC_API_KEY")

    def __init__(self):
        pass


    def bindings(self) -> Dict[str, dict]:
        opt_bindings = config.get("bindings", None)
        catalog = {}
        for b in opt_bindings:
            catalog.update({b['id']: b})
        return catalog
