POETRY=poetry

.PHONY: install lint format test run-all

install:
	$(POETRY) install

lint:
	$(POETRY) run ruff check .

format:
	$(POETRY) run ruff check --fix . || true
	$(POETRY) run black .

test:
	$(POETRY) run pytest -q

run-all:
	$(POETRY) run python run_all.py
