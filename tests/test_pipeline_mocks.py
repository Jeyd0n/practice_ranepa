from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dco_project.domain.schemas import PricingRequest, PricingResult
from dco_project.pipeline.pricing_pipeline import run_pricing_pipeline


def test_pipeline_with_mocked_dependencies() -> None:
    expected_pricing = PricingResult(
        base_price_m2=100000.0,
        recommended_price_m2=110000.0,
        recommended_total_price=5500000.0,
        raw_change_pct=10.0,
        bounded_change_pct=10.0,
        sales_effect_pct=3.0,
        inventory_effect_pct=2.0,
        mortgage_effect_pct=4.0,
        seasonality_effect_pct=1.0,
        comment="mocked",
    )

    request = PricingRequest(
        project_id="MSK-001",
        district="ЮЗАО",
        object_class="комфорт",
        stage="монолит",
        area_m2=50.0,
        month=4,
    )

    with patch(
        "dco_project.pipeline.pricing_pipeline.fetch_mock_project_sales",
        return_value={"fact_sales_month": 99, "unsold_share": 0.11},
    ) as sales_mock, patch(
        "dco_project.pipeline.pricing_pipeline.fetch_mock_sales_plan",
        return_value={"plan_sales_month": 88},
    ) as plan_mock, patch(
        "dco_project.pipeline.pricing_pipeline.fetch_mock_macro_context",
        return_value={"mortgage_rate": 7.7},
    ) as macro_mock, patch(
        "dco_project.pipeline.pricing_pipeline.calculate_price",
        return_value=expected_pricing,
    ) as calc_mock:
        output = run_pricing_pipeline(request)

    sales_mock.assert_called_once_with("MSK-001")
    plan_mock.assert_called_once_with("MSK-001", 4)
    macro_mock.assert_called_once_with(4)
    calc_mock.assert_called_once()

    assert output.model_input.plan_sales_month == 88
    assert output.model_input.fact_sales_month == 99
    assert output.model_input.unsold_share == 0.11
    assert output.model_input.mortgage_rate == 7.7
    assert output.pricing == expected_pricing
