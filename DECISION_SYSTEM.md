# Decision System

Signal-to-Proof is a correlation and causality modeling system connected to the business decisions that make the modeling worth doing.

## Start with the decision

Before selecting a statistical method, define:

- What decision is being made?
- What capital, revenue, customer outcome, or operating commitment is exposed?
- What would being wrong cost?
- What evidence grade is sufficient for this decision?
- What stronger evidence can realistically be acquired?

## Map the behavior

The system then defines the observable progression relevant to that decision.

A generic high-consideration journey may look like:

```text
Exposure
  -> Engagement quality
  -> Product / site validation
  -> Configuration or comparison behavior
  -> Lead / account action
  -> Transaction or retained value
```

The journey is not treated as proof that one stage caused the next. It is the measurement map that determines where evidence can be collected.

## Connect product and UX

Behavioral measurement requires product instrumentation.

Examples:

- event naming and taxonomy;
- persistent identifiers where permitted;
- timestamp integrity;
- exposure and outcome windows;
- session boundaries;
- experiment assignment;
- versioned content or product states;
- friction, completion, abandonment, and repeated-use signals.

UX interpretation should answer where confidence increases, where friction appears, and where people abandon or repeat a step. Those interpretations remain bounded by the evidence grade.

## Connect GTM

A result can change go-to-market action without being causal proof.

For example, a controlled association may justify prioritizing a hypothesis for a test, changing instrumentation, or protecting a high-utility experience while stronger evidence is gathered. It should not be used to claim incremental revenue if the counterfactual is missing.

## Connect economics

Evidence acquisition is itself an investment decision.

Signal-to-Proof compares the estimated cost of a wrong decision with the estimated cost of a stronger test. This allows the system to recommend one of three broad paths:

- **Measure:** continue observational monitoring when stronger proof is not economically justified.
- **Prove:** run a powered test when the decision exposure warrants it.
- **Scale with bounds:** expand only within the scope already supported by causal evidence, while monitoring external validity.

## Connect AI and ML appropriately

AI and ML can increase the speed of hypothesis discovery, pattern detection, segmentation, prediction, and interpretation. They do not waive identification requirements.

Signal-to-Proof therefore keeps a hard boundary between:

```text
Prediction: who or what is likely to move?
Effect: what changed because we intervened?
```

The first can guide where to look. The second requires causal identification.

## Executive output

Every run returns:

- the observed relationship;
- the adjusted relationship where applicable;
- gate results;
- evidence grade;
- allowed claim;
- blocked claim;
- limitations;
- next evidence step;
- economic screen;
- product / UX / GTM implications.

The output is designed for a leadership decision, not only a model review.
