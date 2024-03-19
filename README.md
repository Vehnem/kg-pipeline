# KG-Pipeline

Tooling and Interfacing for Knowledge Graphs Construction.

## Structure

- **core** - core model of the framework
  - **llm** - LLM interfaces (OpenAi, Anthropic, Google)
  - **provenance** - TODO
  - **metrics** - metrics for evaluation
  - **utils** - helper methods
- **tasks** - single kgc tasks and tool interfaces
- **datasets** - input data acquisition and generation
- **tests** - tests with examples
- **ui** - web user intefaces
  - **streamlit.py** starts a simple web interface
- **scripts** - handy scripts for development

## LLM for KG experiments

### RML generation and RML mapping tests

Experiments for the paper "Towards self-configuring Knowledge Graph Construction Pipelines using LLMs - A Case Study with RML"

**Iterate runs and requests LLM (generate RML+repair Turtle)**
```
poetry run pytest -s kg_tests/test_final_experiment.py -k test_final 
```

**Generate Stats for paper**
```
poetry run pytest -s kg_tests/test_final_experiment.py -k test_final 
```

**Inspect statistics and view F1 Scores for metrics**
```
streamlit run kg_ui/execute.py
```

**Final results**
https://akswnc7.informatik.uni-leipzig.de/~mhofer/paper_supplements/eswc24/kgc/

## Config.yaml

see [config.yaml](./config.yaml)

## Install

```
pip install poetry
poetry install
```

## Execute Tests

see [tests](./llm4kg_tests/README.md)

## Install Remote Tools

All tools will be installed under `tools` dir.


RMLMapperJava
```
bash scripts/install-rmlmapperjava.sh
```

## Development Notes

- Currently all resources for RML4LLM are located under `llm4kg_tests/resources/`