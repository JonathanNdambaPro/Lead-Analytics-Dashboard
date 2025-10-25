# Modules Backend

Cette page documente les modules Python du backend de l'application.

## Structure des modules

Le backend est organisé en plusieurs modules :

```
backend/
├── app.py                      # Point d'entrée FastAPI
├── core/
│   ├── config.py              # Configuration globale
│   └── openapi_docs_model.py  # Modèles OpenAPI
└── routers/
    ├── ingestion_leads/       # Ingestion des données
    │   ├── main.py           # Routes d'ingestion
    │   ├── model.py          # Modèles Pydantic
    │   ├── utils.py          # Utilitaires
    │   └── docs.py           # Documentation OpenAPI
    └── transformation/        # Transformations analytiques
        ├── main.py           # Routes de transformation
        └── docs.py           # Documentation OpenAPI
```

## Application principale

### `backend.app`

Point d'entrée de l'application FastAPI.

**Fonctions principales** :

- Configuration de l'application FastAPI
- Enregistrement des routers
- Configuration CORS
- Documentation OpenAPI

**Exemple d'utilisation** :

```python
from backend.app import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Configuration

### `backend.core.config`

Contient la configuration globale de l'application.

**Variables de configuration** :

- Paramètres de connexion Notion
- Configuration de la base de données
- Paramètres de logging
- Configuration CORS

### `backend.core.openapi_docs_model`

Modèles Pydantic pour la documentation OpenAPI.

**Modèles** :

- Schémas de réponse API
- Modèles de données
- Documentation des endpoints

## Routers

### Ingestion des leads

#### `backend.routers.ingestion_leads.main`

Routes pour l'ingestion des données de leads depuis Notion.

**Endpoints** :

- `POST /api/v1/ingestion/leads` : Ingérer des leads
- `GET /api/v1/ingestion/status` : Statut de l'ingestion

**Exemple** :

```python
@router.post("/leads")
async def ingest_leads(leads: List[Lead]):
    """
    Ingère une liste de leads dans Delta Lake.

    Args:
        leads: Liste des leads à ingérer

    Returns:
        Statut de l'ingestion
    """
    # Implémentation
    pass
```

#### `backend.routers.ingestion_leads.model`

Modèles Pydantic pour les leads.

**Modèles** :

```python
class Lead(BaseModel):
    """Modèle d'un lead."""

    id: str
    nom: str
    email: Optional[str]
    telephone: Optional[str]
    date_prise_contact: Optional[datetime]
    date_appel_booke: Optional[datetime]
    date_appel_propose: Optional[datetime]
    date_relance: Optional[datetime]
    date_reponse_prospect: Optional[datetime]
    statut: str
```

#### `backend.routers.ingestion_leads.utils`

Fonctions utilitaires pour l'ingestion.

**Fonctions** :

- `validate_lead()` : Valide un lead
- `transform_notion_data()` : Transforme les données Notion
- `write_to_delta_lake()` : Écrit dans Delta Lake

### Transformation des données

#### `backend.routers.transformation.main`

Routes pour les transformations et agrégations de données.

**Endpoints** :

##### `GET /api/v1/transformation/count_date_by_week`

Retourne le nombre d'événements par semaine.

**Paramètres** : Aucun

**Réponse** :

```json
[
  {
    "semaine": "2025-W01",
    "date_prise_contact": 45,
    "date_reponse_prospect": 32,
    "date_appel_booke": 28,
    "date_appel_propose": 35,
    "date_relance": 40
  }
]
```

**Implémentation** :

```python
@router.get("/count_date_by_week")
async def count_date_by_week() -> List[WeeklyEventCount]:
    """
    Agrège les événements par semaine.

    Utilise une requête SQL avec UNPIVOT pour transformer
    les colonnes de dates en lignes, puis PIVOT pour recréer
    une colonne par type d'événement.

    Returns:
        Liste des comptages par semaine

    Example:
        >>> data = await count_date_by_week()
        >>> print(data[0].semaine)
        "2025-W01"
    """
    # Exécution de la requête SQL
    pass
```

##### `GET /api/v1/transformation/count_date_by_month`

Retourne le nombre d'événements par mois.

**Paramètres** : Aucun

**Réponse** :

```json
[
  {
    "mois": "2025-01",
    "date_prise_contact": 180,
    "date_reponse_prospect": 145,
    "date_appel_booke": 120,
    "date_appel_propose": 150,
    "date_relance": 160
  }
]
```

**Requête SQL utilisée** :

```sql
WITH unpivoted_and_monthly AS (
  SELECT
    DATE_TRUNC('month', date) AS mois,
    type_evenement,
    date
  FROM (
    UNPIVOT DELTA_SCAN('/path/to/data_leads')
    ON date_appel_booke,
       date_appel_propose,
       date_prise_contact,
       date_relance,
       date_reponse_prospect
    INTO
    NAME type_evenement
    VALUE date
  )
  WHERE date IS NOT NULL
)
PIVOT unpivoted_and_monthly
ON type_evenement
USING COUNT(date)
GROUP BY mois
ORDER BY mois;
```

## Format des docstrings

Le projet utilise le format **Google** pour les docstrings :

```python
def exemple_fonction(param1: str, param2: int) -> bool:
    """
    Brève description de la fonction.

    Description détaillée optionnelle de ce que fait
    la fonction.

    Args:
        param1: Description du premier paramètre
        param2: Description du second paramètre

    Returns:
        Description de ce qui est retourné

    Raises:
        ValueError: Si param2 est négatif

    Example:
        >>> resultat = exemple_fonction("test", 42)
        >>> print(resultat)
        True
    """
    if param2 < 0:
        raise ValueError("param2 doit être positif")
    return len(param1) > param2
```

## Dépendances

Le backend utilise les dépendances suivantes :

- **FastAPI** : Framework web
- **DuckDB** : Base de données analytique
- **Delta Lake** : Format de stockage
- **Pydantic** : Validation de données
- **Loguru** : Logging structuré
- **uvicorn** : Serveur ASGI

Pour plus d'informations sur l'API, consultez la [documentation API](api/overview.md).
