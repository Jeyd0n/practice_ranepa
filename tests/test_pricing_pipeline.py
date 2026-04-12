from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dco_project.domain.schemas import PricingRequest
from dco_project.pipeline.pricing_pipeline import run_pricing_pipeline


def test_pipeline_uses_internal_data_sources_and_returns_expected_output() -> None:
    request = PricingRequest(
        project_id="MSK-001",
        district="ЮЗАО",
        object_class="комфорт",
        stage="монолит",
        area_m2=40.0,
        month=4,
    )

    output = run_pricing_pipeline(request)

    assert output.model_input.plan_sales_month == 42
    assert output.model_input.fact_sales_month == 38
    assert output.model_input.unsold_share == 0.52
    assert output.model_input.mortgage_rate == 13.7
    assert output.pricing.recommended_price_m2 == 407850.0
    assert output.pricing.recommended_total_price == 16314000.0
    assert output.pricing.bounded_change_pct == -2.89


def test_pipeline_respects_manual_overrides_in_request() -> None:
    request = PricingRequest(
        project_id="MSK-003",
        district="САО",
        object_class="бизнес",
        stage="отделка",
        area_m2=55.0,
        month=9,
        plan_sales_month=10,
        fact_sales_month=0,
        unsold_share=0.3,
        mortgage_rate=12.0,
    )

    output = run_pricing_pipeline(request)

    assert output.model_input.plan_sales_month == 10
    assert output.model_input.fact_sales_month == 0
    assert output.model_input.unsold_share == 0.3
    assert output.model_input.mortgage_rate == 12.0
    assert output.pricing.recommended_price_m2 == 533295.0
    assert output.pricing.recommended_total_price == 29331208.0
    assert output.pricing.bounded_change_pct == -2.75
