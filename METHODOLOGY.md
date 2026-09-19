# Methodology

## Governing distinction

Correlation and causal inference answer different questions.

**Correlation:** Do two measured variables move together?

**Causal inference:** What changed because the intervention occurred, compared with a defensible counterfactual?

Signal-to-Proof keeps those questions separate throughout the pipeline.

## Correlation

The public demonstrator calculates Pearson and Spearman correlation between exposure and the primary outcome.

Pearson is useful for linear co-movement. Spearman is useful when the relationship is monotonic but not necessarily linear or when rank behavior is more stable than raw scale.

A correlation coefficient is never promoted directly into a causal claim.

## Controlled association

The engine can fit a linear model with declared controls and fixed effects. In the observational scenario, this is used to ask whether the exposure relationship remains after accounting for important measured differences such as baseline demand, media pressure, supply conditions, offer intensity, and time/unit effects.

A controlled model improves comparability. It does not eliminate unobserved confounding or self-selection.

## Selection risk

A central risk in marketing and product-behavior measurement is that people or markets with higher baseline intent are also more likely to receive, discover, or consume the exposure.

The public engine therefore checks the association between baseline-intent variables and exposure. A strong relationship raises a selection warning and lowers the claim ceiling unless a valid counterfactual exists.

The warning threshold in this repository is an illustrative public heuristic, not a production scoring rule.

## Exposure variation

A model cannot identify an exposure relationship if exposure does not vary meaningfully across the analytical units.

For example, if every region receives effectively the same intervention at the same time, unit and time fixed effects may absorb the signal that the analyst hoped to estimate.

Signal-to-Proof therefore treats exposure variation as an explicit gate rather than an after-the-fact caveat.

## Temporal order

Cause must precede effect. In production work this often requires event windows, exposure windows, latency definitions, and outcome windows.

The public demonstrator uses period-level examples. The randomized scenario explicitly separates pre and post periods; the observational scenario remains association-focused and does not claim person-level temporal identification.

## Randomization and counterfactuals

The randomized demo assigns treatment independently of the outcome and evaluates a pre/post intervention design. The counterfactual is represented by units that were eligible for treatment but remained untreated during the experiment.

When assignment integrity, exposure variation, data completeness, and power all pass, the system can allow causal language within the tested scope.

## Power and minimum detectable effect

A null result is not informative when the design is too small to detect the effect leadership actually cares about.

The public power gate estimates the minimum detectable standardized effect for the available treatment and control sizes at the configured alpha and power, then expresses that effect in the outcome's natural units.

The goal is not to maximize statistical significance. It is to know whether the experiment can answer the business question before the organization pays for it.

## Multiple comparisons

This public demonstrator uses one declared primary outcome per scenario. A production program with multiple outcomes, segments, lags, models, or content families should define a multiplicity strategy before broad exploratory matrices are used for decision claims.

## Evidence grades

The public engine uses six grades:

| Grade | What it supports | What it does not support |
|---|---|---|
| Observed signal | The event or behavior was observed | Relationship or effect |
| Directional association | Exposure and outcome move together | Controlled contribution or causality |
| Controlled association | Relationship persists after declared controls | Removal of hidden selection |
| Matched association | Comparable matched units differ under the matching design | Full elimination of selection bias |
| Quasi-experimental estimate | Estimated incremental effect under explicit assumptions | Randomized proof or universal generalization |
| Causal experiment | Treatment changed the measured outcome within the tested design | Automatic generalization to other markets, products, periods, or mechanisms |

## Outcome depth is not causal strength

An exposure linked to a later transaction is a deep business outcome. It is still an observed linkage unless a valid counterfactual establishes what would have happened without the exposure.

Signal-to-Proof therefore keeps two questions separate:

1. How far downstream is the outcome?
2. How strong is the causal design?

## ML and prediction

Predictive models can help prioritize who is likely to act, identify patterns, segment demand, or surface anomalies. Those uses are valuable, but prediction does not identify intervention effect by itself.

In Signal-to-Proof, predictive or synthetic hypotheses sit upstream of causal validation. They can help decide what to test; they do not promote the evidence grade.

## Decision economics

Not every business question deserves the most expensive causal design. The repository includes a transparent economic screen so the cost of better evidence can be compared with the value at risk from a wrong decision.

This is a decision aid, not a universal finance model.

## Reproducibility

Every public demo scenario is deterministic:

- the data-generation seed is fixed;
- the manifest is versioned;
- the pipeline emits structured JSON;
- expected results are stored;
- tests verify key claim boundaries;
- the public-release scanner checks for restricted terms before packaging.
