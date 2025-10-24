import os
from pathlib import Path
from pprint import pprint
from typing import Callable

import polars as pl
from deltalake import DeltaTable, write_deltalake
from model import DataSourceInfos, ListNotionPropertyValues, NotionPropertyValues
from notion_client import Client

# Create a persistent DuckDB database


# Fonctions d'extraction simples
def simple_strategy(prop_data: dict, key: str) -> any:
    """Extrait une valeur simple"""
    return prop_data.get(key)


def list_strategy(prop_data: dict, key: str) -> list:
    """Extrait une liste"""
    return prop_data.get(key, [])


StrategiesPatternPropertiesNotion = Callable[[dict, str], any]
DictStrategiesPatternPropertiesNotion = Callable[[str], StrategiesPatternPropertiesNotion]


# Dictionnaire de stratégies
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
) -> list[NotionPropertyValues]:
    """
    Extrait les valeurs des propriétés Notion

    Args:
        notion_properties: Le dictionnaire 'properties' d'une page Notion

    Returns:
        NotionPropertyValues: Objet contenant uniquement les valeurs
    """
    values = {}
    list_notion_properties = []
    pprint(notion_properties)

    for propertie in notion_properties["results"]:
        for prop_key, prop_data in propertie["properties"].items():
            prop_type = prop_data.get("type")
            values[prop_key] = strategy_properties[prop_type](prop_data)

        values["id"] = propertie["id"]

        list_notion_properties.append(NotionPropertyValues(**values))

    list_notion_properties = ListNotionPropertyValues(list_notion_property_value=list_notion_properties)

    return list_notion_properties


def normalise_data(list_notion_properties: ListNotionPropertyValues) -> list[dict]:
    """
    Normalise les données Notion en format dict simple

    Args:
        list_notion_properties: Liste des propriétés Notion validées

    Returns:
        list[dict]: Liste de dictionnaires normalisés
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


notion = Client(auth=os.environ["NOTION_TOKEN"])
databases_id = os.environ["DATABASE_ID"]

my_page = notion.databases.retrieve(database_id=databases_id)

for data_sources in my_page["data_sources"]:
    if data_sources["name"] == "Leads":
        data_source = DataSourceInfos(**data_sources)

my_data_source = notion.data_sources.query(data_source_id=data_source.id_)


values = extract_property_values(my_data_source)
values_noramalise = normalise_data(values)
pprint(pl.from_dicts(values_noramalise))


def write_to_deltalake(values_noramalise: list[dict]):
    schema = {
        "id": pl.Utf8,
        "activite_source_pharow": pl.Utf8,
        "departement": pl.Utf8,
        "en_croissance": pl.Utf8,
        "genre": pl.Utf8,
        "niveau_hierachique": pl.Utf8,
        "priorite": pl.Utf8,
        "reponse_setting": pl.Utf8,
        "show": pl.Utf8,
        "sous_departement": pl.Utf8,
        "tranche_effectif_corrigee": pl.Utf8,
        "type_de_setting": pl.Utf8,
        "etat": pl.Utf8,
        "adresse_siege_complete": pl.Utf8,
        "chiffre_affaires_simplifie": pl.Utf8,
        "nom": pl.Utf8,
        "nom_entreprise": pl.Utf8,
        "poste_occupe": pl.Utf8,
        "prenom": pl.Utf8,
        "ville_residence": pl.Utf8,
        "nom_du_projet": pl.Utf8,
        "date_appel_booke": pl.Date,
        "date_appel_propose": pl.Date,
        "date_prise_contact": pl.Date,
        "date_relance": pl.Date,
        "date_reponse_prospect": pl.Date,
        "budget": pl.Float64,
        "email_pro": pl.Utf8,
        "telephone": pl.Utf8,
        "url_site_internet": pl.Utf8,
        "url_linkedin": pl.Utf8,
        "personne_assignee": pl.List(pl.Utf8),
    }

    path_table_deltake = Path(__file__).parents[1] / "leads_data"

    data_to_put_un_duckdb = pl.from_dicts(values_noramalise, schema_overrides=schema)

    if not path_table_deltake.exists():
        write_deltalake(path_table_deltake, data_to_put_un_duckdb)
        return

    dt = DeltaTable(path_table_deltake)

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


write_to_deltalake(values_noramalise)
