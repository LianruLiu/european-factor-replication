"""Factor-model specifications.

A model is just a name plus an ordered list of factor columns, e.g.::

    ModelSpec(name="FF5", factors=["Mkt-RF", "SMB", "HML", "RMW", "CMA"])
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ModelSpec:
    """A linear factor model: test-asset excess returns regressed on factors."""

    name: str
    factors: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.factors:
            raise ValueError("a model needs at least one factor")

    @property
    def k(self) -> int:
        return len(self.factors)


#: Fama-French (1993) three-factor model.
FF3 = ModelSpec(name="FF3", factors=["Mkt-RF", "SMB", "HML"])

#: Fama-French (2015) five-factor model.
FF5 = ModelSpec(name="FF5", factors=["Mkt-RF", "SMB", "HML", "RMW", "CMA"])

#: Carhart (1997) four-factor model (adds momentum).
CARHART4 = ModelSpec(name="Carhart4", factors=["Mkt-RF", "SMB", "HML", "MOM"])

#: Single-factor market model (CAPM-style).
CAPM = ModelSpec(name="CAPM", factors=["Mkt-RF"])


def custom_model(name: str, factors: list[str]) -> ModelSpec:
    """Define your own model, e.g. ``custom_model("FF5+MOM", [...])``."""
    return ModelSpec(name=name, factors=list(factors))


def from_config(models_cfg: dict[str, list[str]]) -> list[ModelSpec]:
    """Build model specs from a YAML ``models:`` mapping."""
    return [ModelSpec(name=name, factors=list(cols))
            for name, cols in models_cfg.items()]
