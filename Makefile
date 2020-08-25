venv: requirements.txt
	rm -rf venv
	python3.8 -m venv venv
	venv/bin/pip install -r requirements.txt

.PHONY: lint
lint: venv
	venv/bin/black --config=pyproject.toml .
	venv/bin/mypy --config-file=mypy.ini .

.PHONY: clean
clean:
	rm -rf venv
