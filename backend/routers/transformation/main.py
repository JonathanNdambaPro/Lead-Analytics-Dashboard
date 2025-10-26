from pathlib import Path
from typing import Annotated

import duckdb
from fastapi import APIRouter, Query
from jinja2 import Template
from loguru import logger

from backend.core.config import settings
from backend.routers.transformation import docs

router = APIRouter(prefix="/transformation", tags=["Transformation"])

DATE_COLS = ["date_appel_booke", "date_appel_propose", "date_prise_contact", "date_relance", "date_reponse_prospect"]


@router.get("/count_date_by_week", **docs.count_date_by_week.model_dump())
async def count_date_by_week(
    date_cols: list[str] = DATE_COLS,
    delta_table_path: Annotated[
        str | Path, Query(description="Path to the Delta Lake table", example="data_leads")
    ] = settings.GCS_URI,
):
    """Count date events by week from Delta Lake.

    Aggregates date-based events from the Leads table and returns weekly counts.
    Performs unpivot, date truncation, and pivot operations using DuckDB SQL.

    Args:
        date_cols: List of date column names to include in aggregation.
        delta_table_path: Path to the Delta Lake table to query.

    Returns:
        List of dictionaries with weekly counts per event type.
    """
    logger.info(f"💫 columns to aggregate {date_cols}")

    path_to_folder_request = Path(__file__).parent / "request"
    path_to_count_by_date = path_to_folder_request / "count_by_week_form_deltalake.sql"

    query_template = path_to_count_by_date.read_text(encoding="utf-8")

    template = Template(query_template)
    query = template.render(delta_table_path=delta_table_path, date_cols=date_cols)

    weekly_counts_dict = duckdb.query(query).df().to_dict(orient="records")

    return weekly_counts_dict


@router.get("/count_date_by_month", **docs.count_date_by_month.model_dump())
async def count_date_by_month(
    date_cols: list[str] = DATE_COLS,
    delta_table_path: Annotated[
        str | Path, Query(description="Path to the Delta Lake table", example="data_leads")
    ] = settings.GCS_URI,
):
    """Count date events by week from Delta Lake.

    Aggregates date-based events from the Leads table and returns weekly counts.
    Performs unpivot, date truncation, and pivot operations using DuckDB SQL.

    Args:
        date_cols: List of date column names to include in aggregation.
        delta_table_path: Path to the Delta Lake table to query.

    Returns:
        List of dictionaries with weekly counts per event type.
    """
    logger.info(f"💫 columns to aggregate by month {date_cols}")

    path_to_folder_request = Path(__file__).parent / "request"
    path_to_count_by_date = path_to_folder_request / "count_by_month_form_deltalake.sql"

    query_template = path_to_count_by_date.read_text(encoding="utf-8")

    template = Template(query_template)
    query = template.render(delta_table_path=delta_table_path, date_cols=DATE_COLS)
    logger.info(query)
    monthly_counts_dict = duckdb.query(query).df().to_dict(orient="records")

    return monthly_counts_dict
