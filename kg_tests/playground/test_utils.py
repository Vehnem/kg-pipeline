from kg_core.utils.output_parser import CodeBlockExtractor
from kg_core.utils.log import Logger
import datetime

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

def test_logger():
    log = Logger('test')
    log.info('Hello, World!')
    log.debug('Hello, World!')
    log.error('Hello, World!')
    log.warning('Hello, World!')


def test_datetime_format():
    # create datetime in the form of "YYYY-MM-DD-HH-MM-SS"
    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    print(datetime_str)



test_datetime_format()