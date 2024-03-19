from kg_core.config import Config

config = Config()

def test_config_key():
    assert not config.OPENAI_API_KEY == None


def test_config_bindings():
    print(config.bindings())


def test_config_llm_models():
    print(config.llm_models())