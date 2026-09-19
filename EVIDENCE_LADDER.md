# Evidence Ladder

Signal-to-Proof uses an evidence ladder to prevent a result from inheriting a stronger claim than its design can support.

## 1. Observed signal

**Question:** Did the event happen?

Examples: exposures, views, sessions, configuration starts, lead starts, transactions.

**Allowed:** “The behavior was observed.”

**Blocked:** “The behavior was caused by the intervention.”

## 2. Directional association

**Question:** Do exposure and outcome move together?

Typical methods: correlation, path analysis, cohort comparison.

**Allowed:** “Exposure is associated with the outcome.”

**Blocked:** “Exposure changed the outcome.”

## 3. Controlled association

**Question:** Does the relationship remain after declared measured controls?

Typical methods: regression, fixed effects, lagged models, panel analysis.

**Allowed:** “The relationship remains after the stated controls.”

**Blocked:** “The controlled model proves the intervention caused the outcome.”

## 4. Matched association

**Question:** Do comparable matched units show different outcomes?

Typical methods: exact matching, propensity-based matching, privacy-safe matchback.

**Allowed:** “Matched groups differ under the stated matching design.”

**Blocked:** “Matching removed all selection bias.”

## 5. Quasi-experimental estimate

**Question:** Can a credible counterfactual be constructed without random assignment?

Typical methods: difference-in-differences, synthetic control, regression discontinuity, interrupted time series under defensible assumptions.

**Allowed:** “The design estimates an incremental effect under the stated assumptions.”

**Blocked:** “The estimate is assumption-free causal proof.”

## 6. Causal experiment

**Question:** Did randomized or otherwise controlled treatment change the measured outcome?

Typical methods: randomized holdout, randomized routing, powered geo experiment, randomized staggered rollout.

**Allowed:** “Treatment caused the measured change within the tested design.”

**Blocked:** “The same effect will automatically generalize to all products, audiences, periods, or markets.”

## Two-axis interpretation

Signal-to-Proof separates **outcome depth** from **causal strength**.

```text
OUTCOME DEPTH
Exposure -> Engagement -> Product behavior -> Lead -> Transaction

CAUSAL STRENGTH
Observed -> Association -> Controlled -> Quasi-experimental -> Randomized
```

A transaction match can be deeper in the business funnel while still being weaker causal evidence than a randomized experiment measuring an intermediate outcome.
