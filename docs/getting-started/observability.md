# Observabilité avec Logfire

Ce guide explique comment utiliser Logfire pour monitorer et observer votre application en temps réel.

## Qu'est-ce que Logfire ?

**Logfire** est une plateforme d'observabilité moderne développée par Pydantic qui combine :

- 📊 **Traces distribuées** : Suivi complet des requêtes API
- 🔍 **Logs structurés** : Centralisation et recherche des logs
- ⚡ **Métriques** : Performance et santé de l'application
- 🐛 **Debugging** : Identification rapide des problèmes
- 📈 **Dashboards** : Visualisations automatiques

## Configuration

### 1. Créer un compte Logfire

1. Aller sur [https://logfire.pydantic.dev](https://logfire.pydantic.dev)
2. Créer un compte (offre gratuite disponible)
3. Créer un nouveau projet pour votre application

### 2. Obtenir le token API

1. Dans le dashboard Logfire, naviguer vers **Settings** → **API Keys**
2. Créer une nouvelle API key
3. Copier le token généré

### 3. Ajouter le token à votre environnement

```bash
# Dans votre fichier .env
LOGFIRE_TOKEN=logfire_xxxxxxxxxxxxx
```

### 4. Vérifier l'intégration

L'intégration Logfire est déjà configurée dans le code :

```python
# backend/routers/transformation/main.py
import logfire
from loguru import logger

logfire.configure(token=os.environ["LOGFIRE_TOKEN"])
logger.configure(handlers=[logfire.loguru_handler()])
```

## Utilisation

### Visualiser les logs et traces

Une fois l'application lancée avec le token configuré :

1. Ouvrir [https://logfire.pydantic.dev](https://logfire.pydantic.dev)
2. Sélectionner votre projet
3. Naviguer dans les différentes vues

### Dashboard principal

Le dashboard affiche :

- **Traces** : Liste des requêtes API avec durée et statut
- **Logs** : Flux des logs en temps réel
- **Metrics** : Graphiques de performance
- **Errors** : Alertes et erreurs identifiées

### Recherche et filtrage

Logfire permet de rechercher dans les logs avec des filtres avancés :

```
level:INFO AND message:"weekly aggregation"
duration:>1s
status_code:500
```

### Traces distribuées

Chaque requête API génère une trace avec :

- **Spans** : Étapes détaillées de la requête
- **Tags** : Métadonnées (endpoint, méthode, paramètres)
- **Logs** : Logs associés à la trace
- **Performance** : Durées de chaque étape

## Exemples de logs

### Logs d'agrégation

```
2025-10-26 15:30:12 | INFO | 📊 Starting weekly aggregation for columns: [...]
2025-10-26 15:30:12 | INFO | 📂 Reading from: gs://notion-dataascode/data_leads
2025-10-26 15:30:12 | INFO | ✅ DuckDB connection configured for GCS access
2025-10-26 15:30:13 | INFO | ✅ Weekly aggregation completed: 24 weeks returned
```

### Logs d'ingestion

```
2025-10-26 15:31:00 | INFO | 🚀 Starting Notion leads ingestion...
2025-10-26 15:31:01 | INFO | 📥 Extracting data from Notion...
2025-10-26 15:31:02 | INFO | 🔄 Transforming Notion properties...
2025-10-26 15:31:02 | INFO | ✅ Transformed 150 records
2025-10-26 15:31:03 | INFO | 💾 Writing to Delta Lake...
2025-10-26 15:31:04 | INFO | ✅ Ingestion completed successfully
```

## Métriques disponibles

Logfire collecte automatiquement :

- **Latency** : Temps de réponse des endpoints
- **Throughput** : Nombre de requêtes par seconde
- **Error rate** : Taux d'erreur
- **Database queries** : Performance DuckDB
- **External calls** : Appels Notion et GCS

## Alertes

Vous pouvez configurer des alertes dans Logfire pour :

- Taux d'erreur élevé
- Latence excessive
- Erreurs spécifiques
- Volumes de requêtes anormaux

## Best practices

### 1. Utiliser des logs structurés

```python
logger.info(f"Processing {count} records from {source}")
# ✅ Informations claires avec contexte
```

### 2. Ajouter du contexte aux traces

Les emojis dans les logs facilitent la lecture visuelle :
- 🚀 Début d'opération
- 📊 Traitement de données
- ✅ Succès
- ❌ Erreur
- 📂 Accès fichier/storage

### 3. Monitorer les opérations critiques

Les endpoints suivants sont automatiquement tracés :
- `/api/v1/ingestion/ingestion_leads`
- `/api/v1/transformation/count_date_by_week`
- `/api/v1/transformation/count_date_by_month`

### 4. Analyser les performances

Utilisez Logfire pour identifier :
- Requêtes lentes
- Goulots d'étranglement
- Problèmes de connexion GCS
- Échecs d'authentification

## Troubleshooting

### Token invalide

```
ERROR: Invalid Logfire token
```

**Solution** : Vérifier que `LOGFIRE_TOKEN` est correctement configuré dans `.env`

### Logs non visibles

**Solutions** :
1. Vérifier la connexion internet
2. Vérifier que le token n'a pas expiré
3. Redémarrer l'application

### Performance

Si Logfire impacte les performances :
1. Réduire le niveau de log (WARNING au lieu de INFO)
2. Utiliser le sampling pour les traces
3. Désactiver temporairement en développement

## Ressources

- **Documentation** : [https://docs.pydantic.dev/logfire](https://docs.pydantic.dev/logfire)
- **Dashboard** : [https://logfire.pydantic.dev](https://logfire.pydantic.dev)
- **Support** : [GitHub Issues](https://github.com/pydantic/logfire/issues)

## Prochaines étapes

- [Configuration complète](configuration.md) : Toutes les variables d'environnement
- [Architecture](../architecture.md) : Comprendre l'architecture complète
- [API](../api/overview.md) : Documentation de l'API
