# Configuration

Ce guide explique comment configurer l'application avec les variables d'environnement nécessaires.

## Variables d'environnement

L'application utilise des variables d'environnement pour la configuration. Les données sensibles ne doivent **jamais** être committées dans le code.

### Backend

Le backend nécessite les variables suivantes :

| Variable | Description | Requis | Exemple |
|----------|-------------|--------|---------|
| `NOTION_TOKEN` | Token d'authentification Notion | Oui | `secret_xxxxxxxxxxxxx` |
| `DATABASE_ID` | ID de la base de données Notion | Oui | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `GCS_URI` | URI du bucket GCS pour Delta Lake | Oui | `gs://notion-dataascode/data_leads` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Chemin vers le fichier credentials GCS | Oui | `/path/to/credentials.json` |
| `HMAC_KEY` | Clé HMAC pour l'authentification GCS | Oui | `GOOG1EXXX...` |
| `HMAC_SECRET` | Secret HMAC pour l'authentification GCS | Oui | `your-hmac-secret` |
| `LOGFIRE_TOKEN` | Token Logfire pour l'observabilité | Oui | `logfire_xxxxxxxxxxxxx` |
| `PYTHONUNBUFFERED` | Mode non-bufferisé Python | Non | `1` |

### Frontend

Le frontend nécessite la variable suivante au moment du **build** :

| Variable | Description | Requis | Valeur par défaut |
|----------|-------------|--------|-------------------|
| `NEXT_PUBLIC_API_URL` | URL de l'API backend | Non | `http://localhost:8000` |

!!! warning "Variables NEXT_PUBLIC"
    Les variables préfixées par `NEXT_PUBLIC_` sont injectées dans le code frontend au moment du build et sont visibles côté client. Ne mettez jamais de secrets dans ces variables.

## Configuration pour le développement local

### Créer le fichier .env

Créez un fichier `.env` à la racine du projet :

```bash
# .env
NOTION_TOKEN=secret_xxxxxxxxxxxxx
DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Google Cloud Storage
GCS_URI=gs://notion-dataascode/data_leads
GOOGLE_APPLICATION_CREDENTIALS=/path/to/gcs-credentials.json
HMAC_KEY=GOOG1EXXX...
HMAC_SECRET=your-hmac-secret

# Observabilité
LOGFIRE_TOKEN=logfire_xxxxxxxxxxxxx
```

!!! danger "Important"
    Le fichier `.env` est déjà dans le `.gitignore`. Ne le committez **jamais** !

!!! info "Stockage local vs GCS"
    - **Développement local** : Vous pouvez omettre `GCS_URI` et `GOOGLE_APPLICATION_CREDENTIALS`. Les données seront stockées localement dans `backend/data_leads/`
    - **Production/GCS** : Configurez `GCS_URI` et `GOOGLE_APPLICATION_CREDENTIALS` pour utiliser Google Cloud Storage

### Backend

Le backend charge automatiquement le fichier `.env` si vous utilisez `python-dotenv`.

```bash
# Lancer le backend (charge automatiquement .env)
uv run uvicorn backend.app:app --reload
```

### Frontend

Pour le frontend, créez un fichier `.env.local` dans le dossier `frontend/` :

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

```bash
cd frontend
pnpm dev  # Charge automatiquement .env.local
```

## Configuration avec Docker

### Fichier .env pour Docker Compose

Docker Compose lit automatiquement le fichier `.env` à la racine :

```bash
# .env (à la racine)
NOTION_TOKEN=secret_xxxxxxxxxxxxx
DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Lancer avec Docker

```bash
make docker-deploy
```

### Variables en ligne de commande

Vous pouvez aussi passer les variables directement :

```bash
NOTION_TOKEN=xxx DATABASE_ID=yyy docker-compose up
```

## Configuration pour la production

### Variables d'environnement via build args

Pour le frontend en production, passez l'URL de l'API au build :

```bash
docker build \
  --build-arg NEXT_PUBLIC_API_URL=https://api.example.com \
  -f Dockerfile.frontend \
  -t frontend-prod .
```

### Secrets Docker

Pour la production, utilisez Docker secrets plutôt que des variables d'environnement :

```yaml
# docker-compose.prod.yml
services:
  backend:
    secrets:
      - notion_token
      - database_id

secrets:
  notion_token:
    external: true
  database_id:
    external: true
```

### Gestionnaires de secrets

Pour la production, considérez l'utilisation de :

- **Docker Secrets** : Pour Docker Swarm
- **Kubernetes Secrets** : Pour Kubernetes
- **AWS Secrets Manager** : Pour AWS
- **Azure Key Vault** : Pour Azure
- **HashiCorp Vault** : Solution multi-cloud

## Obtenir les tokens Notion

### 1. Créer une intégration Notion

1. Aller sur [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Cliquer sur "New integration"
3. Donner un nom à votre intégration
4. Copier le "Internal Integration Token" → C'est votre `NOTION_TOKEN`

### 2. Obtenir l'ID de la database

1. Ouvrir votre database dans Notion
2. L'URL ressemble à : `https://www.notion.so/xxxxxxxxxxxx?v=yyyyyyyy`
3. Le `xxxxxxxxxxxx` est votre `DATABASE_ID`

### 3. Donner accès à la database

1. Ouvrir votre database dans Notion
2. Cliquer sur "..." en haut à droite
3. "Add connections" → Sélectionner votre intégration

## Configurer Google Cloud Storage (optionnel)

### 1. Créer un Service Account GCS

1. Aller sur [Google Cloud Console](https://console.cloud.google.com)
2. Créer un nouveau projet ou sélectionner un projet existant
3. Aller dans "IAM & Admin" → "Service Accounts"
4. Créer un Service Account avec les permissions :
   - `Storage Object Admin` (pour lire/écrire dans le bucket)

### 2. Créer et télécharger la clé JSON

1. Cliquer sur le Service Account créé
2. Onglet "Keys" → "Add Key" → "Create new key"
3. Choisir le format JSON
4. Télécharger le fichier JSON → C'est votre fichier credentials

### 3. Créer un bucket GCS

```bash
# Avec la CLI gcloud
gsutil mb -p YOUR_PROJECT_ID gs://notion-dataascode

# Définir les permissions
gsutil iam ch serviceAccount:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT.iam.gserviceaccount.com:roles/storage.objectAdmin gs://notion-dataascode
```

### 4. Configurer les variables d'environnement

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
export GCS_URI="gs://notion-dataascode/data_leads"
export HMAC_KEY="GOOG1EXXX..."
export HMAC_SECRET="your-hmac-secret"
```

## Configurer Logfire (observabilité)

### 1. Créer un compte Logfire

1. Aller sur [https://logfire.pydantic.dev](https://logfire.pydantic.dev)
2. Créer un compte (gratuit pour commencer)
3. Créer un nouveau projet

### 2. Obtenir le token

1. Dans le dashboard Logfire, aller dans "Settings" → "API Keys"
2. Créer une nouvelle API key
3. Copier le token → C'est votre `LOGFIRE_TOKEN`

### 3. Configuration

```bash
export LOGFIRE_TOKEN="logfire_xxxxxxxxxxxxx"
```

### 4. Visualiser les logs et traces

Une fois l'application lancée, tous les logs et traces seront visibles dans le dashboard Logfire :
- URL : [https://logfire.pydantic.dev](https://logfire.pydantic.dev)
- Traces des requêtes API en temps réel
- Logs structurés avec recherche
- Métriques de performance
- Graphiques et dashboards automatiques

## Validation de la configuration

Pour vérifier que votre configuration est correcte :

```bash
# Backend
uv run python -c "import os; print('NOTION_TOKEN:', 'OK' if os.getenv('NOTION_TOKEN') else 'MISSING')"

# Test de connexion à l'API
curl http://localhost:8000/docs
```

## Sécurité

!!! danger "Bonnes pratiques de sécurité"
    - ✅ Utilisez `.env` pour le développement local
    - ✅ Ajoutez `.env` au `.gitignore`
    - ✅ Ajoutez `*credentials*.json` au `.gitignore`
    - ✅ Utilisez des secrets managers en production
    - ✅ Rotez régulièrement les tokens et credentials
    - ✅ Utilisez des Service Accounts avec permissions minimales (least privilege)
    - ❌ Ne committez jamais de secrets dans Git
    - ❌ N'utilisez jamais `ARG` pour les secrets dans Dockerfile
    - ❌ Ne loggez jamais les secrets ou credentials

## Prochaines étapes

- [Docker](docker.md) : Déployer avec Docker
- [API Backend](../api/overview.md) : Utiliser l'API
