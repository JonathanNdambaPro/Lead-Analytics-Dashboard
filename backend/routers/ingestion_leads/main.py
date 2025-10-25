"""Ingestion module for extracting and loading Notion data into Delta Lake.

This module handles the complete ETL process for Notion leads data:
- Extracts data from Notion data sources
- Transforms properties into a normalized format
- Loads data into Delta Lake with merge operations
"""

from fastapi import APIRouter

from backend.routers.ingestion_leads import docs
from backend.routers.ingestion_leads.utils import (
    extract_property_values,
    get_data_source_from_notion,
    normalise_data,
    write_to_deltalake,
)

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])


@router.get("/ingestion_leads", **docs.ingestion_leads.model_dump())
async def ingestion_leads() -> dict[str, str | int]:
    """Ingest Notion Leads data into Delta Lake.

    Extracts data from Notion, transforms it, and loads into Delta Lake.

    Returns:
        Dictionary with success message and record count.
    """
    my_data_source = get_data_source_from_notion()
    values = extract_property_values(my_data_source)
    values_normalise = normalise_data(values)
    write_to_deltalake(values_normalise)

    return {
        "message": "Données notion leads mise à jour",
        "status": "success",
        "records_processed": len(values_normalise),
    }
