.PHONY: install demo-observational demo-randomized test verify

install:
	python -m pip install -e .[dev]

demo-observational:
	python run_demo.py --scenario observational

demo-randomized:
	python run_demo.py --scenario randomized

test:
	pytest -q

verify:
	python scripts/verify_public_release.py
