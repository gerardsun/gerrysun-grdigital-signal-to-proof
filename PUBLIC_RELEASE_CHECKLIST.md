# Public Release Checklist

Before publishing a new version:

- [ ] Run `pytest -q`.
- [ ] Run `python scripts/verify_public_release.py`.
- [ ] Confirm demo datasets are synthetic.
- [ ] Confirm no client names, client systems, client IDs, or confidential schemas appear anywhere.
- [ ] Confirm no private implementation logic or proprietary thresholds were copied into the public branch.
- [ ] Confirm README links resolve.
- [ ] Open `docs/index.html` locally and test desktop and mobile widths.
- [ ] Confirm both demo scenarios execute from a clean environment.
- [ ] Confirm the observational scenario does not emit causal language.
- [ ] Confirm the randomized scenario cannot emit causal language when the counterfactual or power gate is forced to fail.
- [ ] Review `IP_BOUNDARY.md` against the release contents.
- [ ] Create the public repository from this clean directory rather than from any private repository history.
