"""Pydantic models for validating and normalizing Notion data structures.

This module defines the data models used for:
- Validating Notion API responses
- Normalizing nested Notion property structures
- Defining Polars schema for Delta Lake storage
"""

from datetime import date
from typing import Optional

import polars as pl
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

load_dotenv()


class DataSourceInfos(BaseModel):
    """Information about a Notion data source.

    Attributes:
        id_: Unique identifier of the data source.
        name: Human-readable name of the data source.
    """

    id_: str = Field(..., alias="id", serialization_alias="id")
    name: str = Field(..., description="Name of the datasource")


class DateValue(BaseModel):
    """Model for Notion date property values.

    Notion dates can represent single dates or date ranges,
    optionally with timezone information.

    Attributes:
        start: The start date of the date range.
        end: The end date if this is a date range, None for single dates.
        time_zone: IANA timezone identifier (e.g., "America/New_York").
    """

    start: Optional[date] = None
    end: Optional[date] = None
    time_zone: Optional[str] = None


class SelectValue(BaseModel):
    """Model for Notion select and status property values.

    Represents a single option from a select or multi-select property.

    Attributes:
        id: Unique identifier of the select option.
        name: Display name of the option.
        color: Color tag associated with the option (e.g., "blue", "red").
    """

    id: str | None = None
    name: str | None = None
    color: str | None = None


class TextContent(BaseModel):
    """Model for text content within rich text elements.

    Attributes:
        content: The actual text content.
        link: Optional link object if the text is hyperlinked.
    """

    content: str
    link: Optional[dict] = None


class RichText(BaseModel):
    """Model for Notion rich text property elements.

    Rich text in Notion can include formatting, links, and various text types
    (text, mention, equation, etc.).

    Attributes:
        plain_text: Plain text representation without formatting.
        text: Detailed text content object.
        type: Type of rich text element (text, mention, equation).
        href: Direct URL if this text element is a link.
        annotations: Formatting annotations (bold, italic, color, etc.).
    """

    plain_text: str
    text: TextContent
    type: str
    href: Optional[str] = None
    annotations: dict


class NotionPropertyValues(BaseModel):
    """Model for validated Notion property values from Leads database.

    This model extracts and validates the VALUES (not metadata) of all
    properties from a Notion Leads page. Field validators ensure that
    select/date fields have proper default values when None.

    Attributes:
        id_: Unique page identifier.
        activite_source_pharow: Source activity from Pharow system.
        departement: Department selector.
        en_croissance: Growth status selector.
        genre: Gender selector.
        niveau_hierachique: Hierarchical level selector.
        priorite: Priority selector.
        reponse_setting: Setting response selector.
        show: Show selector.
        sous_departement: Sub-department selector.
        tranche_effectif_corrigee: Corrected employee range selector.
        type_de_setting: Setting type selector.
        etat: Current state/status of the lead.
    """

    id_: str = Field(..., alias="id", serialization_alias="id")
    activite_source_pharow: SelectValue | None = Field(None, alias="Activité source Pharow")
    departement: SelectValue | None = Field(None, alias="Département")
    en_croissance: SelectValue | None = Field(None, alias="En croissance")
    genre: SelectValue | None = Field(None, alias="Genre")
    niveau_hierachique: SelectValue | None = Field(None, alias="Niveau hiérachique")
    priorite: SelectValue | None = Field(None, alias="Priorité")
    reponse_setting: SelectValue | None = Field(None, alias="Réponse setting")
    show: SelectValue | None = Field(None, alias="Show")
    sous_departement: SelectValue | None = Field(None, alias="Sous-département")
    tranche_effectif_corrigee: SelectValue | None = Field(None, alias="Tranche d'effectif corrigée")
    type_de_setting: SelectValue | None = Field(None, alias="Type de setting")
    etat: SelectValue | None = Field(None, alias="État")

    # Rich text fields - on récupère la liste
    adresse_siege_complete: list[RichText] = Field(default_factory=list, alias="Adresse du siège complète")
    chiffre_affaires_simplifie: list[RichText] = Field(default_factory=list, alias="Chiffre d'affaires simplifié")
    nom: list[RichText] = Field(default_factory=list, alias="Nom")
    nom_entreprise: list[RichText] = Field(default_factory=list, alias="Nom entreprise")
    poste_occupe: list[RichText] = Field(default_factory=list, alias="Poste occupé")
    prenom: list[RichText] = Field(default_factory=list, alias="Prenom")
    ville_residence: list[RichText] = Field(default_factory=list, alias="Ville de résidence")

    # Title field
    nom_du_projet: list[RichText] = Field(default_factory=list, alias="Nom du projet")

    # Date fields - on récupère l'objet date s'il existe
    date_appel_booke: DateValue | None = Field(None, alias="Date d'appel booké")
    date_appel_propose: DateValue | None = Field(None, alias="Date d'appel proposé")
    date_prise_contact: DateValue | None = Field(None, alias="Date de prise de contact")
    date_relance: DateValue | None = Field(None, alias="Date de relance")
    date_reponse_prospect: DateValue | None = Field(None, alias="Date de réponse du prospect")

    # Number field
    budget: Optional[float] = Field(None, alias="Budget")

    # Email field
    email_pro: Optional[str] = Field(None, alias="Email pro")

    # Phone field
    telephone: Optional[str] = Field(None, alias="Téléphone")

    # URL fields
    url_site_internet: Optional[str] = Field(None, alias="URL du site internet")
    url_linkedin: Optional[str] = Field(None, alias="Url Linkedin")

    # People field
    personne_assignee: list[dict] = Field(default_factory=list, alias="Personne assignée")

    @field_validator("date_appel_booke", "date_appel_propose", "date_relance", mode="before")
    @classmethod
    def date_value(cls, value: str) -> str:
        """Ensure date fields have a DateValue instance.

        Args:
            value: The raw date value from Notion API.

        Returns:
            A DateValue instance, or empty DateValue if value is not already DateValue.
        """
        if not isinstance(value, DateValue):
            value = DateValue()
        return value

    @field_validator(
        "activite_source_pharow",
        "departement",
        "en_croissance",
        "genre",
        "niveau_hierachique",
        "priorite",
        "reponse_setting",
        "show",
        "sous_departement",
        "tranche_effectif_corrigee",
        "type_de_setting",
        "etat",
        mode="before",
    )
    @classmethod
    def capitalize(cls, value: str) -> str:
        """Ensure select/status fields have a SelectValue instance.

        Args:
            value: The raw select value from Notion API.

        Returns:
            A SelectValue instance, or empty SelectValue if value is not already SelectValue.
        """
        if not isinstance(value, SelectValue):
            value = SelectValue()
        return value

    class Config:
        """Pydantic configuration."""

        populate_by_name = True


class ListNotionPropertyValues(BaseModel):
    """Container for multiple validated Notion property value objects.

    Attributes:
        list_notion_property_value: List of validated NotionPropertyValues instances.
    """

    list_notion_property_value: list[NotionPropertyValues]


SCHEMA_POLARS = {
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
