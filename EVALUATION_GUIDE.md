# Evaluation Guide

This repository is designed to be evaluated at three levels.

## 2-minute executive review

Read the first half of [`README.md`](README.md).

Look for four things:

1. Does the system define the decision before the model?
2. Does it separate correlation from causality?
3. Does it block claims the evidence cannot support?
4. Does it translate the result into a next action?

## 10-minute technical review

Open:

- [`ARCHITECTURE.md`](ARCHITECTURE.md)
- [`src/signal_to_proof/gates.py`](src/signal_to_proof/gates.py)
- [`src/signal_to_proof/claims.py`](src/signal_to_proof/claims.py)
- [`src/signal_to_proof/pipeline.py`](src/signal_to_proof/pipeline.py)

Then run:

```bash
pip install -e .[dev]
python run_demo.py --scenario observational
python run_demo.py --scenario randomized
```

The observational run should find a meaningful relationship while refusing a causal claim.

The randomized run should permit causal language only if the counterfactual and power gates pass.

## 20-minute engineering review

Run:

```bash
pytest -q
python scripts/verify_public_release.py
```

Inspect the tests that matter most:

- `test_no_exposure_variation.py`
- `test_no_counterfactual.py`
- `test_underpowered.py`
- `test_randomized_causal_claim.py`
- `test_claim_guard.py`

A useful measurement system should be judged partly by what it refuses to say.

## Questions this repository is designed to answer

- Can the author frame a measurement problem as a decision system?
- Is the data model explicit about grain, keys, controls, and design?
- Are statistics separated from evidence strength?
- Can the code detect identification failures?
- Is causal language gated rather than stylistic?
- Is test power checked before a null result is treated as meaningful?
- Are results translated into business, product, UX, and GTM consequences?
- Is the implementation reproducible and testable?
- Is the public/private IP boundary explicit?

## What this repository intentionally does not prove

The public demonstrator does not claim production readiness for every domain, replace a full causal-inference library, or disclose private production methods. It demonstrates architecture, reasoning discipline, executable controls, and a working reference pipeline using synthetic data.
