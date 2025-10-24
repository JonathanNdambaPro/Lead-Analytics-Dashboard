from datetime import date
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

load_dotenv()


class DataSourceInfos(BaseModel):
    id_: str = Field(..., alias="id", serialization_alias="id")
    name: str = Field(..., description="Name of the datasource")


class DateValue(BaseModel):
    """Modèle pour les valeurs de date"""

    start: Optional[date] = None
    end: Optional[date] = None
    time_zone: Optional[str] = None


class SelectValue(BaseModel):
    """Modèle pour les valeurs select"""

    id: str | None = None
    name: str | None = None
    color: str | None = None


class TextContent(BaseModel):
    """Modèle pour le contenu texte"""

    content: str
    link: Optional[dict] = None


class RichText(BaseModel):
    """Modèle pour rich_text"""

    plain_text: str
    text: TextContent
    type: str
    href: Optional[str] = None
    annotations: dict


class NotionPropertyValues(BaseModel):
    """Modèle pour extraire uniquement les VALEURS des propriétés Notion"""

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
        if not isinstance(value, SelectValue):
            value = SelectValue()
        return value

    class Config:
        populate_by_name = True


class ListNotionPropertyValues(BaseModel):
    list_notion_property_value: list[NotionPropertyValues]
