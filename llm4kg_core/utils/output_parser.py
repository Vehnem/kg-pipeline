import re

def extract_codeblocks_from_markdown(file_path):
    # Read the markdown file
    with open(file_path, 'r') as file:
        markdown_content = file.read()

    # Use regular expressions to find code blocks
    code_blocks = re.findall(r'```.*?```', markdown_content, re.DOTALL)

    # Concatenate the code blocks into a single string
    code_string = '\n'.join(code_blocks)

    return code_string

# Usage example
file_path = '/path/to/markdown/file.md'
code_string = extract_codeblocks_from_markdown(file_path)
print(code_string)
