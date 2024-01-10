# Binding

from dataclasses import dataclass

@dataclass
class BindingConfig:
    dependencies: []
    name: str

class Binding(abs):

    config = None

    def __init__(self, config: BindingConfig) -> None:
        self.config = config

    def run(self):
        pass

