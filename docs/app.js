const data = {
  observational: {
    evidence: "CONTROLLED ASSOCIATION",
    action: "PROVE BEFORE SCALE",
    pearson: "0.706",
    effect: "β 0.00021",
    gates: [
      ["Data completeness", "PASS", "Required fields and grain are available."],
      ["Exposure variation", "PASS", "Exposure varies across units and time."],
      ["Selection risk", "WARN", "Baseline intent is related to exposure."],
      ["Counterfactual", "FAIL", "No randomized counterfactual exists."],
      ["Claim ceiling", "PASS", "Controlled association only."]
    ],
    allowed: "Exposure is associated with the primary outcome after the declared measured controls and fixed effects.",
    blocked: "Exposure caused the observed outcome change or incremental business value.",
    next: "Design a powered holdout or randomized rollout before scaling the claim to incrementality."
  },
  randomized: {
    evidence: "CAUSAL EXPERIMENT",
    action: "SCALE WITH BOUNDS",
    pearson: "0.711",
    effect: "+1.47 pp",
    gates: [
      ["Data completeness", "PASS", "Required fields and grain are available."],
      ["Exposure variation", "PASS", "Treatment creates observable variation."],
      ["Randomization balance", "PASS", "Baseline diagnostic is acceptable."],
      ["Counterfactual", "PASS", "Treatment and control exist across pre/post periods."],
      ["Power", "PASS", "Design can detect the declared business-relevant effect."]
    ],
    allowed: "Within the tested design and period, the randomized intervention caused a measurable change in the primary outcome.",
    blocked: "The intervention will produce the same effect in every market, audience, product, or future period.",
    next: "Replicate in a new eligible population before generalizing beyond the tested scope."
  }
};

function statusClass(s) { return s === "PASS" ? "pass" : s === "WARN" ? "warn" : "fail"; }

function render(key) {
  const d = data[key];
  document.querySelectorAll('.tab').forEach(b => b.classList.toggle('active', b.dataset.scenario === key));
  document.getElementById('evidence-grade').textContent = d.evidence;
  document.getElementById('business-action').textContent = d.action;
  document.getElementById('raw-correlation').textContent = `r = ${d.pearson}`;
  document.getElementById('model-effect').textContent = d.effect;
  document.getElementById('allowed-claim').textContent = d.allowed;
  document.getElementById('blocked-claim').textContent = d.blocked;
  document.getElementById('next-step').textContent = d.next;
  const gates = document.getElementById('gate-list');
  gates.innerHTML = d.gates.map(([name,status,reason]) => `
    <div class="card span-4">
      <div class="status ${statusClass(status)}">${status}</div>
      <h3>${name}</h3>
      <p class="small">${reason}</p>
    </div>`).join('');
  document.querySelectorAll('.rung').forEach(r => r.classList.remove('current'));
  const id = key === 'randomized' ? 'rung-causal' : 'rung-controlled';
  document.getElementById(id).classList.add('current');
}

document.querySelectorAll('.tab').forEach(b => b.addEventListener('click', () => render(b.dataset.scenario)));
render('observational');
