# Guide Docker

Ce guide explique comment utiliser Docker pour développer et déployer l'application.

## Architecture Docker

L'application est composée de deux services containerisés :

- **Backend** : API FastAPI (Python 3.13)
- **Frontend** : Application Next.js (Node.js 20)

Les services communiquent via un réseau Docker dédié.

## Démarrage rapide

### Prérequis

- Docker 20.10+
- Docker Compose 2.0+

### Commandes Make

```bash
# Build et démarrage (tout-en-un)
make docker-deploy

# Ou étape par étape
make docker-build    # Build des images
make docker-up       # Démarrage des conteneurs
make docker-logs     # Voir les logs
make docker-down     # Arrêt des conteneurs
```

## Dockerfiles

### Backend : `Dockerfile.backend`

```dockerfile
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-install-project

COPY . /app
RUN uv sync --frozen

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Caractéristiques** :
- Image légère `python:3.13-slim`
- Utilisation de `uv` pour une installation rapide
- Hot-reload activé en développement
- Variables d'environnement passées au runtime (sécurisé)

### Frontend : `Dockerfile.frontend`

Build multi-stage pour optimiser la taille de l'image :

1. **Stage deps** : Installation des dépendances
2. **Stage builder** : Build de l'application Next.js
3. **Stage runner** : Image de production minimale

**Caractéristiques** :
- Images Alpine légères (~150MB final)
- Utilisateur non-root pour la sécurité
- Mode standalone Next.js
- Variables `NEXT_PUBLIC_*` injectées au build

## Docker Compose

### Configuration

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - NOTION_TOKEN=${NOTION_TOKEN}
      - DATABASE_ID=${DATABASE_ID}
    volumes:
      - ./backend/data_leads:/app/backend/data_leads

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
      args:
        - NEXT_PUBLIC_API_URL=http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

### Services disponibles

Une fois démarrés, les services sont accessibles sur :

- 🌐 **Frontend** : [http://localhost:3000](http://localhost:3000)
- 🔌 **Backend API** : [http://localhost:8000](http://localhost:8000)
- 📚 **Documentation API** : [http://localhost:8000/docs](http://localhost:8000/docs)

## Variables d'environnement

### Fichier .env

Créez un fichier `.env` à la racine :

```bash
# .env
NOTION_TOKEN=secret_xxxxxxxxxxxxx
DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Docker Compose charge automatiquement ce fichier.

### Build args vs ENV

!!! warning "Sécurité"
    - ✅ Utilisez `ENV` au runtime pour les secrets
    - ❌ N'utilisez jamais `ARG` pour les secrets (visible dans l'historique Docker)

**Backend** : Secrets passés via `environment` au runtime

```yaml
environment:
  - NOTION_TOKEN=${NOTION_TOKEN}  # ✅ Sécurisé
```

**Frontend** : URL de l'API passée via `build args` (pas de secret)

```yaml
args:
  - NEXT_PUBLIC_API_URL=http://localhost:8000  # ✅ Pas de secret
```

## Volumes Docker

### Backend

```yaml
volumes:
  - ./backend/data_leads:/app/backend/data_leads
```

Le dossier `data_leads` (Delta Lake) est monté pour persister les données entre les redémarrages.

### Frontend

Pas de volume nécessaire car Next.js est compilé dans l'image.

## Health Checks

Les services ont des health checks configurés :

```yaml
healthcheck:
  test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8000/docs"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

Vérifier le statut :

```bash
docker ps
docker inspect dataascode-backend | grep -A 10 Health
```

## Réseaux

Les services communiquent via un réseau bridge dédié :

```yaml
networks:
  dataascode-network:
    driver: bridge
```

## Logs

### Voir les logs

```bash
# Tous les services
make docker-logs

# Service spécifique
docker logs dataascode-backend
docker logs dataascode-frontend

# Follow mode
docker logs -f dataascode-backend
```

### Logs structurés

Le backend utilise `loguru` pour des logs structurés :

```
2025-10-25 23:36:16.930 | INFO | backend.routers.transformation.main:count_date_by_week:36 - 💫 columns to aggregate
```

## Debugging

### Accéder à un conteneur

```bash
# Backend
docker exec -it dataascode-backend /bin/sh
uv run python

# Frontend
docker exec -it dataascode-frontend /bin/sh
```

### Rebuild après modifications

```bash
# Rebuild complet
make docker-build

# Rebuild sans cache
docker-compose build --no-cache

# Rebuild un seul service
docker-compose build backend
```

## Optimisations

### Cache Docker

Les Dockerfiles utilisent des layers cachés pour accélérer les builds :

1. Copie des fichiers de dépendances d'abord
2. Installation des dépendances (mise en cache)
3. Copie du code source (invalide le cache seulement si le code change)

### .dockerignore

Des fichiers `.dockerignore` spécifiques excluent les fichiers inutiles :

- `Dockerfile.backend.dockerignore` : Exclut `frontend/`
- `Dockerfile.frontend.dockerignore` : Exclut `backend/`

### Taille des images

```bash
# Voir la taille des images
docker images | grep dataascode

# Résultats typiques
dataascode-backend    ~500MB
dataascode-frontend   ~150MB
```

## Production

### Build pour la production

```bash
# Frontend avec URL API personnalisée
docker-compose build \
  --build-arg NEXT_PUBLIC_API_URL=https://api.example.com \
  frontend
```

### Docker Compose production

Créez un `docker-compose.prod.yml` :

```yaml
services:
  backend:
    restart: always
    command: ["uv", "run", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
    # Sans --reload

  frontend:
    restart: always
    environment:
      - NODE_ENV=production
```

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Port déjà utilisé

```bash
# Erreur : bind: address already in use
# Trouver le processus
lsof -i :3000
lsof -i :8000

# Arrêter le processus ou changer le port dans docker-compose.yml
```

### Conteneur ne démarre pas

```bash
# Voir les logs d'erreur
docker logs dataascode-backend

# Vérifier le statut
docker ps -a
```

### Build échoue

```bash
# Rebuild sans cache
docker-compose build --no-cache

# Nettoyer les images
docker system prune -a
```

## Commandes utiles

```bash
# Statut des conteneurs
docker ps

# Arrêter tout
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Nettoyer tout
docker system prune -a --volumes

# Voir l'utilisation des ressources
docker stats
```

## Prochaines étapes

- [API Backend](../api/overview.md) : Utiliser l'API
- [Architecture](../architecture.md) : Comprendre l'architecture
