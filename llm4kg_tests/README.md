# Unit and Integration Tests

## Run Tests

```
poetry run pytest
```

Run single test file
```
poetry run pytest ./path/to/test.py
```

Disbale capturing of stdout
```
poetry run pytest -s ./path/to/test.py
```

Specify matching tests, e.g, on every test name containing util
```
peotry run pytest 
