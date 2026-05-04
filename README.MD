# Структурированный мини-проект ДЦО для московского девелопмента

Учебный mini-production проект для ВУЗа: простая математическая модель + минимальный интерфейс + mock pipeline.

## Что делает проект

Приложение рекомендует цену за м2 и общую цену квартиры на основе:

- района Москвы;
- класса ЖК;
- стадии строительства;
- фактических продаж относительно плана;
- остатка непроданных лотов;
- ипотечной ставки;
- сезонности по месяцу.

Все модели линейные/коэффициентные, без ML и сложной аналитики.

## Технологии

- Python 3.11+
- Streamlit
- Pytest
- Pylint
- GitHub Actions (CI)

## Архитектура

- `app.py` - точка входа Streamlit
- `src/dco_project/ui/streamlit_app.py` - UI слой
- `src/dco_project/pipeline/pricing_pipeline.py` - orchestration/пайплайн
- `src/dco_project/data/mocks.py` - замоканные функции (источники данных)
- `src/dco_project/services/pricing_engine.py` - математический движок ценообразования
- `src/dco_project/domain/schemas.py` - dataclass-модели входа/выхода
- `src/dco_project/config/settings.py` - коэффициенты и параметры модели
- `src/dco_project/config/logging.py` - централизованная настройка логирования
- `tests/test_pricing_pipeline.py` - интеграционные тесты пайплайна
- `.github/workflows/ci.yml` - CI pipeline (test -> build)

## Пайплайн расчёта

1. UI формирует `PricingRequest`.
2. Пайплайн вызывает mock-функции:
`fetch_mock_project_sales`, `fetch_mock_sales_plan`, `fetch_mock_macro_context`.
3. В `ModelInput` собираются данные (mock + ручные override).
4. `pricing_engine` считает рекомендованную цену.
5. UI показывает результат и мета-данные источников.

## Документация и логирование

- В основных функциях добавлены краткие NumPy-style docstring (`Parameters`, `Returns`).
- Добавлен единый модуль логирования: `src/dco_project/config/logging.py`.
- Логи пишутся на этапах UI, mock data, pipeline и pricing engine.

## Запуск

1. Установить зависимости:

```bash
pip install -r requirements.txt
```

2. Запустить интерфейс:

```bash
streamlit run app.py
```

3. Открыть адрес из терминала (обычно `http://localhost:8501`).

## Локальный запуск пайплайна без UI

```bash
PYTHONPATH=src python3 -c "from dco_project.domain.schemas import PricingRequest; from dco_project.pipeline.pricing_pipeline import run_pricing_pipeline; print(run_pricing_pipeline(PricingRequest(project_id='MSK-001', district='ЮЗАО', object_class='комфорт', stage='монолит', area_m2=40, month=4)))"
```

## Тесты

Запуск тестов:

```bash
PYTHONPATH=src python3 -m pytest -q
```

## Линтинг

Проверка только исходников проекта:

```bash
PYTHONPATH=src pylint src --persistent=n
```

Если нужен линт всего проекта:

```bash
PYTHONPATH=src pylint app.py src tests --persistent=n
```

## CI/CD (GitHub Actions)

Workflow: `.github/workflows/ci.yml`

Запускается при изменениях в:
- `app.py`
- `src/**`
- `tests/**`
- `requirements.txt`
- `.github/workflows/**`

Этапы:
1. `test` - запуск `pytest`
2. `build` - compile-check (`python -m compileall ...`) только после успешного `test`

## Пример входных параметров

- `project_id`: `MSK-001`
- `district`: `ЮЗАО`
- `object_class`: `комфорт`
- `stage`: `монолит`
- `area_m2`: `40`
- `month`: `4`

Можно передавать override-поля:
- `plan_sales_month`
- `fact_sales_month`
- `unsold_share`
- `mortgage_rate`

## Примечание

Это учебный пример со структурой, похожей на production, но с моканными данными и упрощённой математикой.
