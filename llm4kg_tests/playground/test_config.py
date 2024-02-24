from llm4kg_core.config import Config

config = Config()


def test_config_key():
    assert not config.OPENAI_API_KEY == None