from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)


def build_observational() -> None:
    rng = np.random.default_rng(37)
    regions = [f"R{idx:02d}" for idx in range(1, 25)]
    weeks = list(range(1, 27))
    region_effect = {r: rng.normal(0, 0.28) for r in regions}
    rows = []

    for region in regions:
        for week in weeks:
            season = 0.35 * math.sin(2 * math.pi * week / 13)
            launch = 1 if 8 <= week <= 12 else 0
            paid = np.clip(rng.normal(0.9 + 0.15 * launch, 0.18), 0.2, 1.6)
            availability = np.clip(rng.normal(0.78 + 0.03 * season, 0.09), 0.35, 1.0)
            offer = np.clip(rng.normal(0.45 + 0.18 * (week >= 18), 0.12), 0.0, 1.0)
            intent = 0.85 + region_effect[region] + season + 0.22 * launch + rng.normal(0, 0.13)
            exposure = 48 + 17 * intent + 10 * paid + 6 * launch + rng.normal(0, 5.0)
            engagement = np.clip(0.30 + 0.0032 * exposure + 0.025 * intent + rng.normal(0, 0.025), 0.05, 0.95)
            configuration = (
                0.035
                + 0.018 * intent
                + 0.00022 * exposure
                + 0.010 * availability
                + 0.004 * offer
                + 0.003 * paid
                + rng.normal(0, 0.0045)
            )
            lead_rate = np.clip(0.010 + 0.42 * configuration + rng.normal(0, 0.003), 0.0, 0.15)
            revenue = max(
                0,
                120000
                + 180000 * configuration
                + 30000 * availability
                + 25000 * offer
                + rng.normal(0, 14000),
            )
            rows.append(
                {
                    "region_id": region,
                    "week_index": week,
                    "education_exposure_index": round(float(exposure), 5),
                    "engagement_quality": round(float(engagement), 6),
                    "configuration_rate": round(float(configuration), 6),
                    "lead_rate": round(float(lead_rate), 6),
                    "revenue_index": round(float(revenue), 2),
                    "baseline_intent_index": round(float(intent), 6),
                    "paid_media_index": round(float(paid), 6),
                    "availability_index": round(float(availability), 6),
                    "offer_index": round(float(offer), 6),
                    "launch_phase": launch,
                }
            )

    pd.DataFrame(rows).to_csv(DATA / "observational_signals.csv", index=False)


def build_randomized() -> None:
    rng = np.random.default_rng(4)
    regions = [f"R{idx:02d}" for idx in range(1, 33)]
    assignment = np.array([0] * 16 + [1] * 16)
    rng.shuffle(assignment)
    treatment_map = dict(zip(regions, assignment.tolist()))
    region_effect = {r: rng.normal(0, 0.0045) for r in regions}
    rows = []

    for region in regions:
        baseline_intent_region = rng.normal(0.0, 0.16)
        for week in range(1, 17):
            post = 1 if week >= 9 else 0
            treatment = treatment_map[region]
            seasonal = 0.003 * math.sin(2 * math.pi * week / 8)
            intent = 0.8 + baseline_intent_region + rng.normal(0, 0.05)
            availability = np.clip(rng.normal(0.82, 0.05), 0.55, 1.0)
            exposure = 20 + rng.normal(0, 2.5) + (42 if treatment and post else 0)
            effect = 0.014 if treatment and post else 0.0
            configuration = (
                0.072
                + region_effect[region]
                + seasonal
                + 0.005 * (intent - 0.8)
                + 0.004 * (availability - 0.82)
                + effect
                + rng.normal(0, 0.0035)
            )
            rows.append(
                {
                    "region_id": region,
                    "week_index": week,
                    "treatment_group": treatment,
                    "post_period": post,
                    "treatment_exposure_index": round(float(exposure), 5),
                    "configuration_rate": round(float(configuration), 6),
                    "baseline_intent_index": round(float(intent), 6),
                    "availability_index": round(float(availability), 6),
                }
            )

    pd.DataFrame(rows).to_csv(DATA / "randomized_signals.csv", index=False)


if __name__ == "__main__":
    build_observational()
    build_randomized()
    print(f"Wrote deterministic demo data to {DATA}")
