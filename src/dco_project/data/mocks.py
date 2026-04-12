from __future__ import annotations

from dco_project.config.logging import get_logger

logger = get_logger(__name__)


def fetch_mock_project_sales(project_id: str) -> dict:
    """Return mocked sales metrics for a project.

    Parameters
    ----------
    project_id : str
        Mock project identifier.

    Returns
    -------
    dict
        Dictionary with ``fact_sales_month`` and ``unsold_share``.
    """
    samples = {
        "MSK-001": {"fact_sales_month": 38, "unsold_share": 0.52},
        "MSK-002": {"fact_sales_month": 56, "unsold_share": 0.41},
        "MSK-003": {"fact_sales_month": 24, "unsold_share": 0.67},
    }
    result = samples.get(project_id, {"fact_sales_month": 35, "unsold_share": 0.55})
    logger.info("Mock sales loaded for project_id=%s: %s", project_id, result)
    return result


def fetch_mock_sales_plan(project_id: str, month: int) -> dict:
    """Return mocked monthly sales plan with season adjustment.

    Parameters
    ----------
    project_id : str
        Mock project identifier.
    month : int
        Month number from 1 to 12.

    Returns
    -------
    dict
        Dictionary with ``plan_sales_month``.
    """
    base_plan = {
        "MSK-001": 40,
        "MSK-002": 52,
        "MSK-003": 30,
    }.get(project_id, 36)

    season_adjust = 1.05 if month in (4, 5, 9, 10) else 0.95 if month in (1, 2, 8) else 1.0
    result = {"plan_sales_month": int(round(base_plan * season_adjust, 0))}
    logger.info(
        "Mock plan loaded for project_id=%s month=%s: %s",
        project_id,
        month,
        result,
    )
    return result


def fetch_mock_macro_context(month: int) -> dict:
    """Return mocked macro context for selected month.

    Parameters
    ----------
    month : int
        Month number from 1 to 12.

    Returns
    -------
    dict
        Dictionary with ``mortgage_rate``.
    """
    month_to_rate = {
        1: 14.4,
        2: 14.2,
        3: 13.9,
        4: 13.7,
        5: 13.5,
        6: 13.4,
        7: 13.6,
        8: 13.8,
        9: 13.5,
        10: 13.3,
        11: 13.2,
        12: 13.4,
    }
    result = {"mortgage_rate": month_to_rate[month]}
    logger.info("Mock macro loaded for month=%s: %s", month, result)
    return result
