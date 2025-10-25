from pathlib import Path
from typing import Callable

import polars as pl
from deltalake import DeltaTable, write_deltalake
from notion_client import Client

from backend.core.config import settings
from backend.routers.ingestion_leads import model

NOTION_CLIENT = Client(auth=settings.NOTION_TOKEN)


def simple_strategy(prop_data: dict, key: str) -> any:
    """Extract a simple value from Notion property data.

    Args:
        prop_data: The property data dictionary from Notion.
        key: The key to extract from the property data.

    Returns:
        The extracted value or None if not found.
    """
    return prop_data.get(key)


def list_strategy(prop_data: dict, key: str) -> list:
    """Extract a list value from Notion property data.

    Args:
        prop_data: The property data dictionary from Notion.
        key: The key to extract from the property data.

    Returns:
        The extracted list or empty list if not found.
    """
    return prop_data.get(key, [])


StrategiesPatternPropertiesNotion = Callable[[dict, str], any]
DictStrategiesPatternPropertiesNotion = Callable[[str], StrategiesPatternPropertiesNotion]


STRATEGIES_PROPERTIES: DictStrategiesPatternPropertiesNotion = {
    "select": lambda data: simple_strategy(data, "select"),
    "status": lambda data: simple_strategy(data, "status"),
    "date": lambda data: simple_strategy(data, "date"),
    "number": lambda data: simple_strategy(data, "number"),
    "email": lambda data: simple_strategy(data, "email"),
    "phone_number": lambda data: simple_strategy(data, "phone_number"),
    "url": lambda data: simple_strategy(data, "url"),
    "rich_text": lambda data: list_strategy(data, "rich_text"),
    "title": lambda data: list_strategy(data, "title"),
    "people": lambda data: list_strategy(data, "people"),
}


def extract_property_values(
    notion_properties: dict, strategy_properties: DictStrategiesPatternPropertiesNotion = STRATEGIES_PROPERTIES
) -> list[model.NotionPropertyValues]:
    """Extract property values from Notion data source results.

    Iterates through all pages in the Notion data source and extracts
    property values using the appropriate strategy for each property type.

    Args:
        notion_properties: Dictionary containing 'results' key with Notion pages.
        strategy_properties: Dictionary mapping property types to extraction strategies.
            Defaults to STRATEGIES_PROPERTIES.

    Returns:
        ListNotionPropertyValues object containing validated property values for all pages.
    """
    values = {}
    list_notion_properties = []

    for propertie in notion_properties["results"]:
        for prop_key, prop_data in propertie["properties"].items():
            prop_type = prop_data.get("type")
            values[prop_key] = strategy_properties[prop_type](prop_data)

        values["id"] = propertie["id"]

        list_notion_properties.append(model.NotionPropertyValues(**values))

    list_notion_properties = model.ListNotionPropertyValues(list_notion_property_value=list_notion_properties)

    return list_notion_properties


def normalise_data(list_notion_properties: model.ListNotionPropertyValues) -> list[dict]:
    """Normalize Notion properties into a flat dictionary structure.

    Transforms complex Notion property structures into simple key-value pairs
    suitable for database storage. Handles nested structures like:
    - Select/Status fields: extracts .name attribute
    - Rich text fields: extracts plain_text from first element
    - Date fields: extracts .start attribute
    - People fields: extracts list of user IDs

    Args:
        list_notion_properties: Validated list of Notion property values.

    Returns:
        List of normalized dictionaries with flat structure ready for database insertion.
    """
    list_values = []

    for notion_properties in list_notion_properties.list_notion_property_value:
        values = {}

        # Select/Status fields - extraire .name si existe
        values["id"] = notion_properties.id_
        values["activite_source_pharow"] = (
            notion_properties.activite_source_pharow.name if notion_properties.activite_source_pharow else None
        )
        values["departement"] = notion_properties.departement.name if notion_properties.departement else None
        values["en_croissance"] = notion_properties.en_croissance.name if notion_properties.en_croissance else None
        values["genre"] = notion_properties.genre.name if notion_properties.genre else None
        values["niveau_hierachique"] = (
            notion_properties.niveau_hierachique.name if notion_properties.niveau_hierachique else None
        )
        values["priorite"] = notion_properties.priorite.name if notion_properties.priorite else None
        values["reponse_setting"] = (
            notion_properties.reponse_setting.name if notion_properties.reponse_setting else None
        )
        values["show"] = notion_properties.show.name if notion_properties.show else None
        values["sous_departement"] = (
            notion_properties.sous_departement.name if notion_properties.sous_departement else None
        )
        values["tranche_effectif_corrigee"] = (
            notion_properties.tranche_effectif_corrigee.name if notion_properties.tranche_effectif_corrigee else None
        )
        values["type_de_setting"] = (
            notion_properties.type_de_setting.name if notion_properties.type_de_setting else None
        )
        values["etat"] = notion_properties.etat.name if notion_properties.etat else None

        # Rich text fields - extraire plain_text ou laisser liste vide
        values["adresse_siege_complete"] = (
            notion_properties.adresse_siege_complete[0].plain_text if notion_properties.adresse_siege_complete else None
        )
        values["chiffre_affaires_simplifie"] = (
            notion_properties.chiffre_affaires_simplifie[0].plain_text
            if notion_properties.chiffre_affaires_simplifie
            else None
        )
        values["nom"] = notion_properties.nom[0].plain_text if notion_properties.nom else None
        values["nom_entreprise"] = (
            notion_properties.nom_entreprise[0].plain_text if notion_properties.nom_entreprise else None
        )
        values["poste_occupe"] = (
            notion_properties.poste_occupe[0].plain_text if notion_properties.poste_occupe else None
        )
        values["prenom"] = notion_properties.prenom[0].plain_text if notion_properties.prenom else None
        values["ville_residence"] = (
            notion_properties.ville_residence[0].plain_text if notion_properties.ville_residence else None
        )
        values["nom_du_projet"] = (
            notion_properties.nom_du_projet[0].plain_text if notion_properties.nom_du_projet else None
        )

        # Date fields - extraire .start si existe
        values["date_appel_booke"] = (
            notion_properties.date_appel_booke.start if notion_properties.date_appel_booke else None
        )
        values["date_appel_propose"] = (
            notion_properties.date_appel_propose.start if notion_properties.date_appel_propose else None
        )
        values["date_prise_contact"] = (
            notion_properties.date_prise_contact.start if notion_properties.date_prise_contact else None
        )
        values["date_relance"] = notion_properties.date_relance.start if notion_properties.date_relance else None
        values["date_reponse_prospect"] = (
            notion_properties.date_reponse_prospect.start if notion_properties.date_reponse_prospect else None
        )

        # Simple fields
        values["budget"] = notion_properties.budget
        values["email_pro"] = notion_properties.email_pro
        values["telephone"] = notion_properties.telephone
        values["url_site_internet"] = notion_properties.url_site_internet
        values["url_linkedin"] = notion_properties.url_linkedin

        # People field
        values["personne_assignee"] = (
            [p.get("id") for p in notion_properties.personne_assignee] if notion_properties.personne_assignee else []
        )

        list_values.append(values)

    return list_values


def get_data_source_from_notion(databases_id: str = settings.DATABASE_ID, notion_client: Client = NOTION_CLIENT):
    """Retrieve Leads data source from a Notion database.

    Fetches the database metadata, finds the "Leads" data source,
    and queries all records from that data source.

    Args:
        databases_id: The ID of the Notion database to query.
            Defaults to DATABASE_ID from environment.
        notion_client: Authenticated Notion client instance.
            Defaults to NOTION_CLIENT.

    Returns:
        Dictionary containing query results with all pages from the Leads data source.

    Raises:
        UnboundLocalError: If no data source named "Leads" is found in the database.
    """
    my_page = notion_client.databases.retrieve(database_id=databases_id)

    for data_sources in my_page["data_sources"]:
        if data_sources["name"] == "Leads":
            data_source = model.DataSourceInfos(**data_sources)

    my_data_source = notion_client.data_sources.query(data_source_id=data_source.id_)

    return my_data_source


def write_to_deltalake(
    values_normalise: list[dict],
    schema: dict = model.SCHEMA_POLARS,
    path_table_deltalake: Path = settings.PATH_DELTALAKE,
) -> None:
    """Write normalized data to Delta Lake with upsert logic.

    Creates a new Delta table if it doesn't exist, or performs a merge operation
    on existing data. After merge, optimizes the table by compacting files
    and cleaning up old versions.

    The merge operation:
    - Matches on 'id' field
    - Updates all columns except 'id' when matched
    - No insert operation for new records (update-only mode)

    Args:
        values_normalise: List of normalized dictionaries to write.
        schema: Polars schema definition for type enforcement.
            Defaults to model.SCHEMA_POLARS.

    Returns:
        None

    Note:
        Vacuum operation uses retention_hours=0 which immediately removes
        old files. This is suitable for development but should be adjusted
        for production use.
    """
    path_table_deltalake = Path(__file__).parents[2] / "data_leads"

    data_to_put_un_duckdb = pl.from_dicts(values_normalise, schema_overrides=schema)

    if not path_table_deltalake.exists():
        write_deltalake(path_table_deltalake, data_to_put_un_duckdb)
        return

    dt = DeltaTable(path_table_deltalake)

    (
        dt.merge(
            source=data_to_put_un_duckdb,
            predicate="target.id = source.id",
            source_alias="source",
            target_alias="target",
        )
        .when_matched_update_all(except_cols=["id"])
        .execute()
    )

    dt.optimize.compact()
    dt.vacuum(retention_hours=0, enforce_retention_duration=False, dry_run=False)
