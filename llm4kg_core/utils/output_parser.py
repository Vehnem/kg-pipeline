import re

class CodeBlockExtractor:

    def __init__(self) -> None:
        pass

    def extract_codeblocks_from_markdown(self, markdown_content):
        code_blocks = re.findall(r'```(?:\w+\n)?(.*?)```', markdown_content, re.DOTALL)
        code_string = '\n'.join(code_blocks).strip()
        return code_string
