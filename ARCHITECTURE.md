# Architecture

Signal-to-Proof is organized around a simple principle: **the system should never inherit a stronger conclusion than the weakest evidence gate supporting it.**

## 1. Decision layer

Every run begins with a decision brief rather than a model choice.

The brief captures:

- the decision leadership is considering;
- the primary business outcome;
- the value or investment exposed to the decision;
- the cost of acquiring stronger evidence;
- the acceptable evidence level for the decision.

This keeps the analytical work tied to a real commitment rather than an isolated metric.

## 2. Evidence manifest

The manifest declares the measurement contract before analysis:

- dataset location;
- native grain;
- unit and time keys;
- exposure variable;
- outcome variable;
- controls;
- design type;
- treatment and post-period indicators when applicable;
- fixed effects;
- primary hypothesis;
- economic inputs.

The manifest is validated before any model runs.

## 3. Correlation layer

The public engine calculates:

- Pearson correlation;
- Spearman correlation;
- controlled linear association;
- lagged correlation diagnostics;
- treatment effect estimates for the randomized demonstration.

These outputs are measurements, not evidence grades by themselves.

## 4. Identification layer

The engine asks whether the observed relationship can plausibly isolate the intervention.

Public demonstration checks include:

- exposure variation;
- missing controls;
- selection-risk diagnostics;
- counterfactual availability;
- treatment assignment structure;
- pre/post coverage;
- power / minimum detectable effect;
- outcome and exposure completeness.

A failed gate changes what the system is allowed to say.

## 5. Evidence grading layer

The engine assigns one of six public evidence grades:

```text
Observed signal
      ↓
Directional association
      ↓
Controlled association
      ↓
Matched association
      ↓
Quasi-experimental estimate
      ↓
Causal experiment
```

The grade is a property of the evidence design, not a reward for model complexity.

## 6. Claim guard

For every result, the engine emits:

- `allowed_claim`
- `blocked_claim`
- `claim_ceiling`
- `limitations`
- `next_evidence_step`

A model can return a statistically strong relationship and still be prevented from using causal language.

## 7. Decision economics

The public demonstrator includes a transparent value-of-information screen:

```text
Expected decision loss = decision exposure × error-cost fraction × uncertainty fraction
```

A proposed test can then be compared with the expected decision loss it may reduce.

This is intentionally simple and inspectable. It shows the connection between statistical evidence and capital allocation without pretending that every decision needs the most expensive possible experiment.

## 8. Product, UX, and GTM interpretation

The output is translated into four operating lenses:

- **Product:** what instrumentation or experience change is required;
- **UX:** what progression, friction, or confidence signal should be observed;
- **GTM:** what should change in audience, message, channel, offer, or rollout;
- **Business:** whether to scale, test, redesign, maintain, or stop.

These translations do not increase the evidence grade. They make the evidence actionable.

## 9. Repository architecture

```text
DecisionBrief
    |
    v
EvidenceManifest ----> Schema validation
    |                         |
    v                         v
DataLoader ------------> Readiness gates
    |                         |
    v                         v
Correlation ---------> Identification checks
    |                         |
    +------------+------------+
                 |
                 v
          Evidence grader
                 |
                 v
            Claim guard
                 |
                 v
       Test / action recommender
                 |
                 v
        Structured result JSON
```

## 10. Public implementation boundary

The repository demonstrates the architecture without disclosing private production logic. Public gate criteria are intentionally transparent and limited. They are suitable for technical evaluation and education, not a substitute for a domain-specific production measurement system.
