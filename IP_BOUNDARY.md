# Public / Private IP Boundary

Signal-to-Proof is a **public technical demonstrator**, not a release of the complete GRDigital measurement system.

## Included publicly

The repository includes enough implementation detail to evaluate the quality of the architecture and engineering:

- evidence-manifest pattern;
- schema validation;
- synthetic demonstration data;
- correlation and controlled-association examples;
- randomized pre/post effect estimation;
- public evidence grades;
- exposure-variation and selection diagnostics;
- power / minimum-detectable-effect check;
- claim guard;
- next-test recommendation logic;
- reproducible tests;
- static technical walkthrough.

## Intentionally excluded

The repository does not include:

- confidential or client data;
- client-specific schemas or taxonomies;
- production connectors;
- private research archives;
- proprietary scoring systems;
- proprietary thresholds or calibration logic;
- internal orchestration or operating artifacts;
- private prompt, routing, or review mechanics;
- production identity-resolution logic;
- domain-specific production rules;
- commercial implementation details that would make omitted private components reverse-engineerable.

## Public implementation note

The gate criteria in this repository are intentionally transparent and simplified for evaluation. A production measurement system should adapt identification strategy, statistical assumptions, privacy controls, power design, multiplicity handling, and decision thresholds to the domain and data-generating process.

## No client lineage in the public package

The demonstration is generic by design. The data, entities, business scenario, code names, and outputs are synthetic and do not reproduce any client dataset or confidential implementation.
