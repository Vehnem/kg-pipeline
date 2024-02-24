# KG-Pipeline

Tooling and Interfacing for Knowledge Graphs Construction

## Structure

- **core** - core model of the framework
  - **llm** - LLM interfaces
  - **provenance** - 
  - **metrics** - 
  - **utils** - helper methods
- **tasks** - single kgc tasks and tool interfaces
  - 
- **datasets** - input data acquisition and generation
  - **utils** - 
  - **acquisition** -
  - **sampling** - 
- **tests** - tests with examples
- **ui** - web user intefaces
  - **streamlit.py** starts a simple web interface
- **scripts** - handy scripts for development

## Config.yaml

see [config.yaml](./config.yaml)

## Install


```
pip install poetry
poetry install
```

## Execute Tests

see [tests](./llm4kg_tests/README.md)
