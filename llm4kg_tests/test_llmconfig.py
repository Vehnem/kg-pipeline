from llm4kg_core.llm.llmconfig import LLMConfig

def test_loadl_llm_config():
    """
    Test the LLMConfig class
    """

    config = LLMConfig("llm4kg_tests/test_config.yaml")
    assert config.openai_key == "1234"
    assert config.not_used == None
    assert config.data == "./target"