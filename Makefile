# PyPerf-AI-CLI Makefile
# Cross-platform build automation

.PHONY: help install test clean build lint demo

PYTHON := python3
PIP := pip3

help:
	@echo "PyPerf-AI-CLI Build Commands"
	@echo "  make install    Install package in development mode"
	@echo "  make test       Run unit tests"
	@echo "  make demo       Run built-in performance demo"
	@echo "  make lint       Run code linting"
	@echo "  make clean      Clean build artifacts"
	@echo "  make build      Build distribution packages"

install:
	$(PIP) install -e .

test:
	$(PYTHON) -m unittest tests.test_profiler -v

demo:
	$(PYTHON) -m pyperf_ai --demo

demo-profile:
	$(PYTHON) -m pyperf_ai examples/demo_slow.py --tui

lint:
	$(PYTHON) -m py_compile pyperf_ai/*.py
	@echo "✅ Syntax check passed"

clean:
	rm -rf build/ dist/ *.egg-info __pycache__ .pytest_cache
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -delete
	@echo "✅ Cleaned build artifacts"

build: clean
	$(PYTHON) setup.py sdist bdist_wheel
	@echo "✅ Build complete"
