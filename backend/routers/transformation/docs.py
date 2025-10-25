"""OpenAPI documentation for transformation endpoints."""

from backend.core.openapi_docs_model import OpenApiDocs

count_date_by_week = OpenApiDocs(
    summary="Count date events by week from Delta Lake",
    description=(
        "Transformation endpoint that aggregates date-based events from the Leads Delta Lake table "
        "and returns weekly counts. The process includes:\n\n"
        "1. **Load**: Reads data from Delta Lake table\n"
        "2. **Transform**: Converts date columns to datetime format\n"
        "3. **Aggregate**: Executes SQL query to unpivot date columns and count by week\n"
        "4. **Return**: Returns aggregated data as a list of dictionaries\n\n"
        "The SQL transformation performs:\n"
        "- UNPIVOT: Transforms date columns into rows (melt operation)\n"
        "- DATE_TRUNC: Groups dates by week (Monday as week start)\n"
        "- PIVOT: Transforms event types back into columns with counts\n\n"
        "This endpoint is useful for weekly activity dashboards and time-series analysis."
    ),
    response_description="List of weekly aggregated date event counts",
    responses={
        200: {
            "description": "Successfully aggregated data by week",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "semaine": "2025-09-29T00:00:00",
                            "date_prise_contact": 1,
                            "date_reponse_prospect": 0,
                            "date_appel_booke": 0,
                            "date_appel_propose": 0,
                            "date_relance": 0,
                        },
                        {
                            "semaine": "2025-10-06T00:00:00",
                            "date_prise_contact": 1,
                            "date_reponse_prospect": 1,
                            "date_appel_booke": 2,
                            "date_appel_propose": 1,
                            "date_relance": 0,
                        },
                    ]
                }
            },
        },
        404: {
            "description": "Delta Lake table not found",
            "content": {"application/json": {"example": {"detail": "Delta table 'data_leads' does not exist"}}},
        },
        500: {
            "description": "Internal server error during transformation",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "DuckDB query execution failed",
                        "error": "Binder Error: Cannot unpivot columns",
                    }
                }
            },
        },
    },
    openapi_extra={
        "tags": ["Transformation"],
        "operationId": "count_date_events_by_week",
        "parameters": [
            {
                "name": "date_cols",
                "in": "query",
                "description": "List of date column names to include in the aggregation",
                "required": False,
                "schema": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": [
                        "date_appel_booke",
                        "date_appel_propose",
                        "date_prise_contact",
                        "date_relance",
                        "date_reponse_prospect",
                    ],
                },
                "style": "form",
                "explode": True,
            },
            {
                "name": "delta_table_path",
                "in": "query",
                "description": "Path to the Delta Lake table to query",
                "required": False,
                "schema": {"type": "string", "default": "data_leads", "example": "data_leads"},
            },
        ],
    },
)
