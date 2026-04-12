from __future__ import annotations

import streamlit as st

from dco_project.config.logging import get_logger
from dco_project.config.settings import CLASS_FACTOR, DISTRICT_BASE_PRICE, STAGE_FACTOR
from dco_project.domain.schemas import PricingRequest
from dco_project.pipeline.pricing_pipeline import run_pricing_pipeline

logger = get_logger(__name__)


def run_app() -> None:
    """Run Streamlit UI for the dynamic pricing pipeline."""
    logger.info("Streamlit UI initialized")
    st.set_page_config(page_title="ДЦО Девелопмент Москва", page_icon="🏗️", layout="centered")
    st.title("Динамическое ценообразование: учебный mini-production")
    st.caption("Пайплайн: UI -> mocks -> model input -> pricing engine -> result")

    with st.form("pricing_form"):
        project_id = st.selectbox("Проект", ["MSK-001", "MSK-002", "MSK-003"])
        district = st.selectbox("Район Москвы", list(DISTRICT_BASE_PRICE.keys()))
        object_class = st.selectbox("Класс объекта", list(CLASS_FACTOR.keys()))
        stage = st.selectbox("Стадия проекта", list(STAGE_FACTOR.keys()))
        month = st.slider("Месяц (1-12)", min_value=1, max_value=12, value=4, step=1)
        area_m2 = st.number_input("Площадь квартиры, м²", min_value=18.0, max_value=250.0, value=42.0)

        st.subheader("Ручные override (необязательно)")
        use_mocks_only = st.checkbox("Использовать только моканные значения", value=True)

        if use_mocks_only:
            plan_sales_month = None
            fact_sales_month = None
            unsold_share = None
            mortgage_rate = None
        else:
            plan_sales_month = st.number_input("План продаж за месяц (лоты)", min_value=1, max_value=500, value=40)
            fact_sales_month = st.number_input("Факт продаж за месяц (лоты)", min_value=0, max_value=500, value=38)
            unsold_share = st.slider("Доля непроданных лотов", min_value=0.05, max_value=0.95, value=0.52, step=0.01)
            mortgage_rate = st.slider("Средняя ипотечная ставка, %", min_value=6.0, max_value=25.0, value=14.0, step=0.1)

        submitted = st.form_submit_button("Запустить пайплайн ДЦО")

    if not submitted:
        st.write("Заполните параметры и нажмите `Запустить пайплайн ДЦО`.")
        return

    logger.info("UI form submitted: project_id=%s month=%s", project_id, month)
    request = PricingRequest(
        project_id=project_id,
        district=district,
        object_class=object_class,
        stage=stage,
        area_m2=float(area_m2),
        month=int(month),
        plan_sales_month=int(plan_sales_month) if plan_sales_month is not None else None,
        fact_sales_month=int(fact_sales_month) if fact_sales_month is not None else None,
        unsold_share=float(unsold_share) if unsold_share is not None else None,
        mortgage_rate=float(mortgage_rate) if mortgage_rate is not None else None,
    )
    output = run_pricing_pipeline(request)
    result = output.pricing
    model_input = output.model_input
    logger.info(
        "UI received pricing result: rec_price_m2=%s total_price=%s",
        result.recommended_price_m2,
        result.recommended_total_price,
    )

    col1, col2 = st.columns(2)
    col1.metric("Базовая цена, ₽/м²", f"{result.base_price_m2:,.0f}".replace(",", " "))
    col2.metric(
        "Рекомендованная цена, ₽/м²",
        f"{result.recommended_price_m2:,.0f}".replace(",", " "),
        delta=f"{result.bounded_change_pct:.2f}%",
    )
    st.metric("Рекомендованная цена квартиры, ₽", f"{result.recommended_total_price:,.0f}".replace(",", " "))

    st.subheader("Факторы модели")
    st.write(f"- Продажи vs план: **{result.sales_effect_pct:+.2f}%**")
    st.write(f"- Остаток непроданных: **{result.inventory_effect_pct:+.2f}%**")
    st.write(f"- Ипотечная ставка: **{result.mortgage_effect_pct:+.2f}%**")
    st.write(f"- Сезонность: **{result.seasonality_effect_pct:+.2f}%**")
    st.write(f"- Итого (до ограничения): **{result.raw_change_pct:+.2f}%**")
    st.write(f"- Итого (с ограничением ±15%): **{result.bounded_change_pct:+.2f}%**")
    st.info(result.comment)

    st.subheader("Что попало в итоговый пайплайн")
    st.json(
        {
            "model_input": model_input.__dict__,
            "meta": output.meta.__dict__,
        }
    )
