# Makefile for running tests, make sure to use llmenv python environment

PYTHON=python
TEST_DIR=tests

.PHONY: test clean

test:
	$(PYTHON) -m pytest $(TEST_DIR)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache