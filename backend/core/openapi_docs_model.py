from pydantic import BaseModel


class OpenApiDocs(BaseModel):
    """
    Documentation for the receive endpoint
    """

    summary: str = ""
    description: str = ""
    response_description: str = ""
    responses: dict = {}
    openapi_extra: dict = {}
