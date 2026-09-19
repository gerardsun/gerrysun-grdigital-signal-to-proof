# Demo Walkthrough

## Scenario A: Observational association

**Business question:** Should a company increase investment in educational product content because regions with greater exposure also show stronger high-intent product behavior?

**What the data contain:**

- exposure index;
- engagement quality;
- high-intent configuration behavior;
- baseline intent;
- paid media pressure;
- supply availability;
- offer intensity;
- launch timing;
- region and week.

**Expected analytical pattern:**

1. Raw exposure and high-intent behavior are positively correlated.
2. Baseline intent is also related to exposure.
3. A controlled model reduces the apparent exposure relationship.
4. No true counterfactual exists.
5. The claim ceiling remains controlled association.

**Correct conclusion:** the relationship is useful and may justify a test, but it does not establish incremental effect.

Run:

```bash
python run_demo.py --scenario observational
```

## Scenario B: Randomized intervention

**Business question:** Did a randomized intervention change high-intent product behavior during the test period?

**What the data contain:**

- randomly assigned treatment group;
- pre and post periods;
- outcome rate;
- region and week;
- stable background controls.

**Expected analytical pattern:**

1. Treatment and control have comparable pre-period behavior.
2. Treatment receives the intervention only in the post period.
3. A difference-in-differences estimate identifies the incremental change.
4. The power gate checks whether the design could detect a decision-relevant effect.
5. If the gate passes, causal language is allowed within the tested scope.

Run:

```bash
python run_demo.py --scenario randomized
```

## Read the output in this order

1. `decision`
2. `economics`
3. `correlation`
4. `controlled_model` or `causal_estimate`
5. `gates`
6. `evidence_grade`
7. `allowed_claim`
8. `blocked_claim`
9. `next_evidence_step`
10. `operating_implications`

The statistical result is intentionally in the middle rather than at the end.

## Rebuild the demo fixtures

The demonstration datasets are deterministic and can be regenerated from source:

```bash
python demo/generate_demo_data.py
python scripts/build_expected_outputs.py
pytest -q
```
