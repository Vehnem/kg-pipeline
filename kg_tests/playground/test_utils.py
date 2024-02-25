from llm4kg_core.utils.output_parser import CodeBlockExtractor

def test_codeblock_extractor():

    extractor = CodeBlockExtractor()

    markdown_content = """
    ```python
    print("Hello, World!")
    ```
    """

    code_string = extractor.extract_codeblocks_from_markdown(markdown_content)

    assert code_string == 'print("Hello, World!")'

    markdown_content_2 = """
    ```
    print("Hello, World!")
    ```
    """

    code_string_2 = extractor.extract_codeblocks_from_markdown(markdown_content_2)

    assert code_string_2 == 'print("Hello, World!")'

    
def test_files():
    print(__file__)
    pass