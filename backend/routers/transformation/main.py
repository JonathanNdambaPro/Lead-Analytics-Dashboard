import os
from pathlib import Path
from typing import Annotated

import duckdb
import logfire
from fastapi import APIRouter, Depends, Query
from jinja2 import Template
from loguru import logger

from backend.core.config import settings
from backend.routers.transformation import docs

logfire.configure(token=os.environ["LOGFIRE_TOKEN"])
logger.configure(handlers=[logfire.loguru_handler()])

router = APIRouter(prefix="/transformation", tags=["Transformation"])

DATE_COLS = ["date_appel_booke", "date_appel_propose", "date_prise_contact", "date_relance", "date_reponse_prospect"]


def get_duckdb_connection():
    """Create a DuckDB connection with GCS credentials configured.

    This is a FastAPI dependency that creates a DuckDB connection,
    configures it for GCS access, and ensures proper cleanup.

    Yields:
        DuckDB connection with GCS support enabled.
    """
    conn = duckdb.connect()

    try:
        # Install and load httpfs extension for GCS support
        conn.execute("INSTALL httpfs;")
        conn.execute("LOAD httpfs;")
        conn.execute(f"""
        CREATE SECRET (
            TYPE gcs,
            KEY_ID '{settings.HMAC_KEY}',
            SECRET '{settings.HMAC_SECRET}'
        );
        """)

        logger.info("✅ DuckDB connection configured for GCS access")
        yield conn

    finally:
        conn.close()
        logger.info("🔒 DuckDB connection closed")


ConnectionDuckDb = Annotated[duckdb.DuckDBPyConnection, Depends(get_duckdb_connection)]


@router.get("/count_date_by_week", **docs.count_date_by_week.model_dump())
async def count_date_by_week(
    date_cols: list[str] = DATE_COLS,
    delta_table_path: Annotated[
        str | Path, Query(description="Path to the Delta Lake table", example="data_leads")
    ] = settings.GCS_URI,
    conn: ConnectionDuckDb = None,
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
    logger.info(f"📊 Starting weekly aggregation for columns: {date_cols}")
    logger.info(f"📂 Reading from: {delta_table_path}")

    path_to_folder_request = Path(__file__).parent / "request"
    path_to_count_by_date = path_to_folder_request / "count_by_week_form_deltalake.sql"

    query_template = path_to_count_by_date.read_text(encoding="utf-8")

    template = Template(query_template)
    query = template.render(delta_table_path=delta_table_path, date_cols=date_cols)

    logger.info("🔍 Executing weekly aggregation query...")
    weekly_counts_dict = conn.query(query).df().to_dict(orient="records")
    logger.info(f"✅ Weekly aggregation completed: {len(weekly_counts_dict)} weeks returned")

    return weekly_counts_dict


@router.get("/count_date_by_month", **docs.count_date_by_month.model_dump())
async def count_date_by_month(
    date_cols: list[str] = DATE_COLS,
    delta_table_path: Annotated[
        str | Path, Query(description="Path to the Delta Lake table", example="data_leads")
    ] = settings.GCS_URI,
    conn: ConnectionDuckDb = None,
):
    """Count date events by month from Delta Lake.

    Aggregates date-based events from the Leads table and returns monthly counts.
    Performs unpivot, date truncation, and pivot operations using DuckDB SQL.

    Args:
        date_cols: List of date column names to include in aggregation.
        delta_table_path: Path to the Delta Lake table to query.

    Returns:
        List of dictionaries with monthly counts per event type.
    """
    logger.info(f"📊 Starting monthly aggregation for columns: {date_cols}")
    logger.info(f"📂 Reading from: {delta_table_path}")

    path_to_folder_request = Path(__file__).parent / "request"
    path_to_count_by_date = path_to_folder_request / "count_by_month_form_deltalake.sql"

    query_template = path_to_count_by_date.read_text(encoding="utf-8")

    template = Template(query_template)
    query = template.render(delta_table_path=delta_table_path, date_cols=DATE_COLS)

    logger.info("🔍 Executing monthly aggregation query...")
    monthly_counts_dict = conn.query(query).df().to_dict(orient="records")
    logger.info(f"✅ Monthly aggregation completed: {len(monthly_counts_dict)} months returned")

    return monthly_counts_dict
