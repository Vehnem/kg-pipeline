import yaml
import os

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

OPENAI= config.get("openai", None)
OPENAI_API_KEY = OPENAI.get("api-key", None)

ANTHROPIC = config.get("anthropic", None)
ANTHROPIC_API_KEY = ANTHROPIC.get("api-key", None)

class Config:
    OPENAI_API_KEY = OPENAI_API_KEY if OPENAI_API_KEY else os.environ("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = ANTHROPIC_API_KEY if ANTHROPIC_API_KEY else os.environ("ANTHROPIC_API_KEY")