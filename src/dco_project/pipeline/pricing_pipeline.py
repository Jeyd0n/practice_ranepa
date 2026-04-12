from __future__ import annotations

from dco_project.config.logging import get_logger
from dco_project.data.mocks import (
    fetch_mock_macro_context,
    fetch_mock_project_sales,
    fetch_mock_sales_plan,
)
from dco_project.domain.schemas import (
    ModelInput,
    PipelineMeta,
    PipelineOutput,
    PricingRequest,
)
from dco_project.services.pricing_engine import calculate_price

logger = get_logger(__name__)


def run_pricing_pipeline(request: PricingRequest) -> PipelineOutput:
    """Execute full pricing pipeline from request to final output.

    Parameters
    ----------
    request : PricingRequest
        User or API request for pricing.

    Returns
    -------
    PipelineOutput
        Final object containing normalized input, result and metadata.
    """
    logger.info("Pipeline started for project_id=%s month=%s", request.project_id, request.month)
    mock_sales = fetch_mock_project_sales(request.project_id)
    mock_plan = fetch_mock_sales_plan(request.project_id, request.month)
    mock_macro = fetch_mock_macro_context(request.month)

    model_input = ModelInput(
        district=request.district,
        object_class=request.object_class,
        stage=request.stage,
        area_m2=request.area_m2,
        plan_sales_month=request.plan_sales_month
        if request.plan_sales_month is not None
        else mock_plan["plan_sales_month"],
        fact_sales_month=request.fact_sales_month
        if request.fact_sales_month is not None
        else mock_sales["fact_sales_month"],
        unsold_share=request.unsold_share if request.unsold_share is not None else mock_sales["unsold_share"],
        mortgage_rate=request.mortgage_rate
        if request.mortgage_rate is not None
        else mock_macro["mortgage_rate"],
        month=request.month,
    )
    logger.info("ModelInput prepared: %s", model_input)

    pricing = calculate_price(model_input)
    meta = PipelineMeta(
        market_source="mock_macro_service",
        sales_source="mock_sales_service",
        plan_source="mock_plan_service",
        used_mock_functions=[
            "fetch_mock_project_sales",
            "fetch_mock_sales_plan",
            "fetch_mock_macro_context",
        ],
    )
    output = PipelineOutput(model_input=model_input, pricing=pricing, meta=meta)
    logger.info("Pipeline finished for project_id=%s", request.project_id)
    return output
