"""Ingestion module for extracting and loading Notion data into Delta Lake.

This module handles the complete ETL process for Notion leads data:
- Extracts data from Notion data sources
- Transforms properties into a normalized format
- Loads data into Delta Lake with merge operations
"""

import os

import logfire
from fastapi import APIRouter
from loguru import logger

from backend.routers.ingestion_leads import docs
from backend.routers.ingestion_leads.utils import (
    extract_property_values,
    get_data_source_from_notion,
    normalise_data,
    write_to_deltalake,
)

logfire.configure(token=os.environ["LOGFIRE_TOKEN"])
logger.configure(handlers=[logfire.loguru_handler()])

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])


@router.get("/ingestion_leads", **docs.ingestion_leads.model_dump())
async def ingestion_leads() -> dict[str, str | int]:
    """Ingest Notion Leads data into Delta Lake.

    Extracts data from Notion, transforms it, and loads into Delta Lake.

    Returns:
        Dictionary with success message and record count.
    """

    logger.info("🚀 Starting Notion leads ingestion...")

    logger.info("📥 Extracting data from Notion...")
    my_data_source = get_data_source_from_notion()

    logger.info("🔄 Transforming Notion properties...")
    values = extract_property_values(my_data_source)
    values_normalise = normalise_data(values)
    logger.info(f"✅ Transformed {len(values_normalise)} records")

    logger.info("💾 Writing to Delta Lake...")
    write_to_deltalake(values_normalise)
    logger.info("✅ Ingestion completed successfully")

    return {
        "message": "Données notion leads mise à jour",
        "status": "success",
        "records_processed": len(values_normalise),
    }
