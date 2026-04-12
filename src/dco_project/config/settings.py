"""Static configuration for the dynamic pricing model.

Notes
-----
Values are intentionally simple and deterministic for a study project.
"""

DISTRICT_BASE_PRICE = {
    "ЦАО": 620_000,
    "САО": 410_000,
    "СВАО": 380_000,
    "ВАО": 350_000,
    "ЮВАО": 330_000,
    "ЮАО": 360_000,
    "ЮЗАО": 420_000,
    "ЗАО": 460_000,
    "СЗАО": 440_000,
    "ТиНАО": 240_000,
}

CLASS_FACTOR = {
    "комфорт": 1.00,
    "бизнес": 1.25,
    "премиум": 1.65,
}

STAGE_FACTOR = {
    "котлован": 0.93,
    "монолит": 1.00,
    "отделка": 1.07,
    "сдан": 1.12,
}

MONTH_SEASONALITY = {
    1: -0.020,
    2: -0.015,
    3: 0.005,
    4: 0.010,
    5: 0.015,
    6: 0.000,
    7: -0.010,
    8: -0.015,
    9: 0.010,
    10: 0.015,
    11: 0.005,
    12: -0.005,
}

TARGET_UNSOLD_SHARE = 0.45
NEUTRAL_MORTGAGE_RATE = 12.0
MAX_ABS_MONTHLY_CHANGE = 0.15
