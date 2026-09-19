from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any
import numpy as np


class GateStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EvidenceGrade(str, Enum):
    OBSERVED_SIGNAL = "OBSERVED_SIGNAL"
    DIRECTIONAL_ASSOCIATION = "DIRECTIONAL_ASSOCIATION"
    CONTROLLED_ASSOCIATION = "CONTROLLED_ASSOCIATION"
    MATCHED_ASSOCIATION = "MATCHED_ASSOCIATION"
    QUASI_EXPERIMENTAL = "QUASI_EXPERIMENTAL"
    CAUSAL_EXPERIMENT = "CAUSAL_EXPERIMENT"


@dataclass(frozen=True)
class GateResult:
    name: str
    status: GateStatus
    reason: str
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["status"] = self.status.value
        return _json_safe(out)


def _json_safe(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    return value
