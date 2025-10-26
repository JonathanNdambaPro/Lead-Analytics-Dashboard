# API Backend

L'API backend est construite avec FastAPI et fournit des endpoints pour l'ingestion et la transformation des données de leads.

## Documentation interactive

L'API dispose d'une documentation interactive Swagger/OpenAPI accessible une fois le serveur lancé :

- **Swagger UI** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc** : [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON** : [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## Base URL

```
http://localhost:8000
```

En production, remplacez par votre domaine.

## Routes disponibles

### Racine

```http
GET /
```

Retourne des informations sur l'API.

**Réponse** :
```json
{
  "message": "Lead Analytics API",
  "version": "0.0.1",
  "docs": "/docs"
}
```

### Transformation - Comptage par semaine

```http
GET /api/v1/transformation/count_date_by_week
```

Retourne le nombre d'événements agrégés par semaine.

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

**Événements suivis** :
- `date_prise_contact` : Première prise de contact avec le lead
- `date_reponse_prospect` : Réponse du prospect
- `date_appel_booke` : Appel effectivement réalisé
- `date_appel_propose` : Appel proposé au prospect
- `date_relance` : Relance du prospect

### Transformation - Comptage par mois

```http
GET /api/v1/transformation/count_date_by_month
```

Retourne le nombre d'événements agrégés par mois.

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

## Architecture SQL

### Requêtes DuckDB

L'API utilise DuckDB pour des agrégations performantes sur Delta Lake :

```sql
WITH unpivoted_and_weekly AS (
  SELECT
    DATE_TRUNC('week', date) AS semaine,
    type_evenement,
    date
  FROM (
    UNPIVOT DELTA_SCAN('gs://notion-dataascode/data_leads')
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
PIVOT unpivoted_and_weekly
ON type_evenement
USING COUNT(date)
GROUP BY semaine
ORDER BY semaine;
```

**Opérations** :
1. **UNPIVOT** : Transforme les colonnes de dates en lignes
2. **DATE_TRUNC** : Agrège par semaine ou mois
3. **PIVOT** : Recrée une colonne par type d'événement
4. **COUNT** : Compte les événements par période

### Delta Lake sur GCS

Les données sont stockées au format Delta Lake sur Google Cloud Storage :

- Versioning des données
- Time travel
- ACID transactions
- Schema evolution
- Compression Snappy
- Stockage cloud distribué et durable
- Accès concurrent sécurisé via GCS

## Format des dates

Toutes les dates suivent le format ISO 8601 :

- **Semaine** : `YYYY-Www` (ex: `2025-W01`)
- **Mois** : `YYYY-MM` (ex: `2025-01`)
- **Date complète** : `YYYY-MM-DD` (ex: `2025-01-15`)

## Codes de statut HTTP

| Code | Signification |
|------|---------------|
| 200 | Succès |
| 400 | Erreur de requête (paramètres invalides) |
| 404 | Ressource non trouvée |
| 500 | Erreur serveur interne |

## Erreurs

Format des erreurs :

```json
{
  "detail": "Description de l'erreur"
}
```

## CORS

Le backend accepte les requêtes CORS de toutes les origines en développement. En production, configurez les origines autorisées dans `backend/core/config.py`.

## Exemples d'utilisation

### cURL

```bash
# Comptage par semaine
curl http://localhost:8000/api/v1/transformation/count_date_by_week

# Comptage par mois
curl http://localhost:8000/api/v1/transformation/count_date_by_month
```

### JavaScript/TypeScript

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// Récupérer les données hebdomadaires
const weeklyData = await api.get('/api/v1/transformation/count_date_by_week');
console.log(weeklyData.data);

// Récupérer les données mensuelles
const monthlyData = await api.get('/api/v1/transformation/count_date_by_month');
console.log(monthlyData.data);
```

### Python

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(
        "http://localhost:8000/api/v1/transformation/count_date_by_week"
    )
    data = response.json()
    print(data)
```

## Performance

### Temps de réponse typiques

- Comptage par semaine : ~50-100ms
- Comptage par mois : ~30-80ms

### Optimisations

- Utilisation de DuckDB pour les agrégations SQL
- Format Delta Lake avec compression Snappy
- Requêtes SQL optimisées avec UNPIVOT/PIVOT
- Pas de cache (temps réel)

## Logging et Observabilité

### Logfire + Loguru

L'API utilise **Logfire** pour l'observabilité complète et **Loguru** pour les logs structurés :

```python
import logfire
from loguru import logger

logfire.configure(token=os.environ["LOGFIRE_TOKEN"])
logger.configure(handlers=[logfire.loguru_handler()])

logger.info("📊 Starting weekly aggregation...")
```

**Fonctionnalités** :
- Logs structurés avec emojis pour la lisibilité
- Traces distribuées des requêtes FastAPI
- Métriques de performance en temps réel
- Corrélation automatique des logs et traces
- Dashboard Logfire pour la visualisation

**Exemple de logs** :
```
2025-10-26 15:30:12 | INFO | 📊 Starting weekly aggregation for columns: [...]
2025-10-26 15:30:12 | INFO | 📂 Reading from: gs://notion-dataascode/data_leads
2025-10-26 15:30:12 | INFO | ✅ DuckDB connection configured for GCS access
2025-10-26 15:30:13 | INFO | ✅ Weekly aggregation completed: 24 weeks returned
```

**Dashboard Logfire** :
- URL : [https://logfire.pydantic.dev](https://logfire.pydantic.dev)
- Visualisation des traces en temps réel
- Recherche et filtrage des logs
- Graphiques de performance automatiques

## Prochaines étapes

- [Modules Backend](../modules.md) : Documentation détaillée des modules
- [Architecture](../architecture.md) : Comprendre l'architecture complète
