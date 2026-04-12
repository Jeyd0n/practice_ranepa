from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PricingRequest:
    """External request for the pricing pipeline.

    Parameters
    ----------
    project_id : str
        Mock project identifier.
    district : str
        Moscow district.
    object_class : str
        Real-estate class (comfort, business, premium).
    stage : str
        Construction stage.
    area_m2 : float
        Apartment area in square meters.
    month : int
        Month number from 1 to 12.
    """

    project_id: str
    district: str
    object_class: str
    stage: str
    area_m2: float
    month: int
    plan_sales_month: int | None = None
    fact_sales_month: int | None = None
    unsold_share: float | None = None
    mortgage_rate: float | None = None


@dataclass
class ModelInput:
    """Normalized input used by the mathematical pricing engine."""

    district: str
    object_class: str
    stage: str
    area_m2: float
    plan_sales_month: int
    fact_sales_month: int
    unsold_share: float
    mortgage_rate: float
    month: int


@dataclass
class PricingResult:
    """Result produced by the pricing model."""

    base_price_m2: float
    recommended_price_m2: float
    recommended_total_price: float
    raw_change_pct: float
    bounded_change_pct: float
    sales_effect_pct: float
    inventory_effect_pct: float
    mortgage_effect_pct: float
    seasonality_effect_pct: float
    comment: str


@dataclass
class PipelineMeta:
    """Metadata about data sources used in pipeline execution."""

    market_source: str
    sales_source: str
    plan_source: str
    used_mock_functions: list[str]


@dataclass
class PipelineOutput:
    """Final pipeline output with input snapshot and pricing result."""

    model_input: ModelInput
    pricing: PricingResult
    meta: PipelineMeta
