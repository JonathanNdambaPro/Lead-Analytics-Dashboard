"""OpenAPI documentation for ingestion endpoints."""

from backend.core.openapi_docs_model import OpenApiDocs

ingestion_leads = OpenApiDocs(
    summary="Ingest Notion Leads data into Delta Lake",
    description=(
        "ETL endpoint that extracts leads data from Notion, transforms it into a normalized format, "
        "and loads it into a Delta Lake table. The process includes:\n\n"
        "1. **Extract**: Fetches data from the 'Leads' data source in Notion\n"
        "2. **Transform**: Normalizes complex Notion properties into flat structures\n"
        "3. **Load**: Performs an upsert operation into the Delta Lake table\n\n"
        "This endpoint is idempotent and can be called multiple times safely. "
        "Existing records are updated based on their ID, and the Delta table is optimized after each run."
    ),
    response_description="Confirmation message indicating successful data ingestion",
    responses={
        200: {
            "description": "Data successfully ingested and loaded into Delta Lake",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Données notion leads mise à jour",
                        "status": "success",
                        "records_processed": 2,
                    }
                }
            },
        },
        401: {
            "description": "Authentication failed - invalid or missing Notion API credentials",
            "content": {
                "application/json": {"example": {"detail": "NOTION_TOKEN environment variable not set or invalid"}}
            },
        },
        404: {
            "description": "Notion data source not found",
            "content": {
                "application/json": {
                    "example": {"detail": "No data source named 'Leads' found in the specified database"}
                }
            },
        },
        500: {
            "description": "Internal server error during ETL process",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to write to Delta Lake", "error": "IO Error: Cannot open file"}
                }
            },
        },
    },
    openapi_extra={
        "tags": ["Ingestion"],
        "operationId": "ingest_notion_leads",
    },
)
