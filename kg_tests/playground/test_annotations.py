from llm4kg_core.utils.annotation import deprecated, todo

@deprecated("Use the new add_numbers function instead.")
def add(a, b):
    """Add two numbers together.

    Args:
        a (int): The first number to add.
        b (int): The second number to add.

    Returns:
        int: The sum of a and b.
    """
    return a + b

@todo()
def todo_add(a, b):
    """Add two numbers together.

    Args:
        a (int): The first number to add.
        b (int): The second number to add.

    Returns:
        int: The sum of a and b.
    """
    return a + b

@deprecated("Use the new greet method instead.")
class Greeter:
    """A simple class for greeting.

    Deprecated:
        Use the new greet method instead.

    Attributes:
        name (str): The name to greet.
    """
    
    def __init__(self, name):
        """
        Args:
            name (str): The name to use in the greeting.
        """
        self.name = name

    def greet(self):
        """Greet the person by name."""
        print(f"Hello, {self.name}!")

def test_deprecated():
    add(1, 2)
    Greeter("John").greet()


def test_todo():
    todo_add(1,2)