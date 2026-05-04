"""Core mathematical engine for dynamic pricing."""

from __future__ import annotations

from dco_project.config.logging import get_logger
from dco_project.config.settings import (
    CLASS_FACTOR,
    DISTRICT_BASE_PRICE,
    MAX_ABS_MONTHLY_CHANGE,
    MONTH_SEASONALITY,
    NEUTRAL_MORTGAGE_RATE,
    STAGE_FACTOR,
    TARGET_UNSOLD_SHARE,
)
from dco_project.domain.schemas import ModelInput, PricingResult

logger = get_logger(__name__)


def _clip(value: float, low: float, high: float) -> float:
    """Clip numeric value into an interval.

    Parameters
    ----------
    value : float
        Input value.
    low : float
        Lower bound.
    high : float
        Upper bound.

    Returns
    -------
    float
        Clipped value.
    """
    return max(low, min(value, high))


def calculate_price(model_input: ModelInput) -> PricingResult:  # pylint: disable=too-many-locals
    """Calculate recommended apartment price using simple math factors.

    Parameters
    ----------
    model_input : ModelInput
        Fully prepared input for pricing calculation.

    Returns
    -------
    PricingResult
        Model output with recommended prices and factor impacts.
    """
    logger.info(
        "Pricing calculation started: district=%s class=%s stage=%s month=%s",
        model_input.district,
        model_input.object_class,
        model_input.stage,
        model_input.month,
    )
    district_price = DISTRICT_BASE_PRICE[model_input.district]
    base_price_m2 = (
        district_price
        * CLASS_FACTOR[model_input.object_class]
        * STAGE_FACTOR[model_input.stage]
    )

    plan = max(model_input.plan_sales_month, 1)
    sales_gap = (model_input.fact_sales_month - plan) / plan
    sales_effect_pct = _clip(0.12 * sales_gap, -0.06, 0.06)

    inventory_gap = model_input.unsold_share - TARGET_UNSOLD_SHARE
    inventory_effect_pct = _clip(-0.15 * inventory_gap, -0.07, 0.07)

    rate_gap = model_input.mortgage_rate - NEUTRAL_MORTGAGE_RATE
    mortgage_effect_pct = _clip(-0.010 * rate_gap, -0.05, 0.05)

    seasonality_effect_pct = MONTH_SEASONALITY[model_input.month]

    raw_change_pct = (
        sales_effect_pct
        + inventory_effect_pct
        + mortgage_effect_pct
        + seasonality_effect_pct
    )

    bounded_change_pct = _clip(
        raw_change_pct,
        -MAX_ABS_MONTHLY_CHANGE,
        MAX_ABS_MONTHLY_CHANGE,
    )
    recommended_price_m2 = base_price_m2 * (1 + bounded_change_pct)
    recommended_total_price = recommended_price_m2 * model_input.area_m2

    if bounded_change_pct > 0.04:
        comment = "Рекомендуется повышение цены: спрос выше цели."
    elif bounded_change_pct < -0.04:
        comment = "Рекомендуется снижение цены: нужно ускорить продажи."
    else:
        comment = "Рекомендуется удерживать цену вблизи текущего уровня."

    result = PricingResult(
        base_price_m2=round(base_price_m2, 0),
        recommended_price_m2=round(recommended_price_m2, 0),
        recommended_total_price=round(recommended_total_price, 0),
        raw_change_pct=round(raw_change_pct * 100, 2),
        bounded_change_pct=round(bounded_change_pct * 100, 2),
        sales_effect_pct=round(sales_effect_pct * 100, 2),
        inventory_effect_pct=round(inventory_effect_pct * 100, 2),
        mortgage_effect_pct=round(mortgage_effect_pct * 100, 2),
        seasonality_effect_pct=round(seasonality_effect_pct * 100, 2),
        comment=comment,
    )
    logger.info(
        "Pricing calculation finished: rec_price_m2=%s change_pct=%s",
        result.recommended_price_m2,
        result.bounded_change_pct,
    )
    return result
