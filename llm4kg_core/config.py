import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

OPENAI= config.get("openai", None)

OPENAI_API_KEY = OPENAI.get("api-key", None)
print(OPENAI_API_KEY)

OPENAI_TEST = OPENAI.get("test", None)
print(OPENAI_TEST)