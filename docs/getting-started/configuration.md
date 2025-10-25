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
```

!!! danger "Important"
    Le fichier `.env` est déjà dans le `.gitignore`. Ne le committez **jamais** !

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
    - ✅ Utilisez des secrets managers en production
    - ✅ Rotez régulièrement les tokens
    - ❌ Ne committez jamais de secrets dans Git
    - ❌ N'utilisez jamais `ARG` pour les secrets dans Dockerfile
    - ❌ Ne loggez jamais les secrets

## Prochaines étapes

- [Docker](docker.md) : Déployer avec Docker
- [API Backend](../api/overview.md) : Utiliser l'API
