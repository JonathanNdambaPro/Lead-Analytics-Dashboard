# 🐳 Guide Docker

Ce document explique comment déployer l'application avec Docker et Docker Compose.

## Prérequis

- Docker (>= 20.10)
- Docker Compose (>= 2.0)

## Architecture

L'application est composée de deux services :

- **Backend** : API FastAPI (Python) sur le port `8000`
- **Frontend** : Application Next.js sur le port `3000`

## Déploiement rapide

### Avec Make (recommandé)

```bash
# Build et démarrage des conteneurs
make docker-deploy

# Voir les logs
make docker-logs

# Arrêter les conteneurs
make docker-down
```

### Avec Docker Compose

```bash
# Build des images
docker-compose build

# Démarrage des services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

## Configuration

### Variables d'environnement

#### Frontend

La variable `NEXT_PUBLIC_API_URL` doit être configurée au moment du build pour pointer vers l'API backend.

**Par défaut** : `http://localhost:8000`

Pour personnaliser :

```bash
docker-compose build --build-arg NEXT_PUBLIC_API_URL=http://votre-api.com frontend
```

#### Backend

Le backend n'a pas besoin de configuration spéciale pour l'instant. Les données sont stockées dans `backend/data_leads` qui est monté comme volume.

## Services disponibles

Une fois les conteneurs démarrés :

- **Frontend** : <http://localhost:3000>
- **Backend API** : <http://localhost:8000>
- **Documentation API** : <http://localhost:8000/docs>

## Build des images individuelles

### Backend

```bash
docker build -t dataascode-backend -f backend/Dockerfile .
docker run -p 8000:8000 -v $(pwd)/backend/data_leads:/app/backend/data_leads dataascode-backend
```

### Frontend

```bash
cd frontend
docker build -t dataascode-frontend --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 .
docker run -p 3000:3000 dataascode-frontend
```

## Optimisations

### Taille des images

Les Dockerfiles utilisent une approche multi-stage pour minimiser la taille des images finales :

- **Frontend** : Build avec Node.js Alpine, runtime optimisé (~150MB)
- **Backend** : Python slim avec uv pour une installation rapide des dépendances

### Sécurité

- Utilisation d'utilisateurs non-root dans les conteneurs
- Images basées sur Alpine Linux (surface d'attaque réduite)
- Pas d'exposition de secrets ou fichiers sensibles

### Performance

- Cache des dépendances optimisé
- Health checks configurés pour chaque service
- Network bridge dédié pour la communication inter-services

## Troubleshooting

### Le frontend ne peut pas contacter le backend

Vérifiez que `NEXT_PUBLIC_API_URL` est correctement configuré. Cette variable doit être définie au moment du build.

```bash
# Rebuild avec la bonne URL
docker-compose build --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 frontend
docker-compose up -d frontend
```

### Les changements de code ne sont pas pris en compte

Les images Docker sont statiques. Vous devez rebuild après chaque modification :

```bash
make docker-build
make docker-up
```

### Erreur de permissions sur data_leads

Assurez-vous que le répertoire `backend/data_leads` a les bonnes permissions :

```bash
chmod -R 755 backend/data_leads
```

## Développement vs Production

### Développement local

Pour le développement, utilisez plutôt :

```bash
make deploy_local
```

Cela lance les serveurs avec hot-reload activé.

### Production

Pour la production, les Dockerfiles sont optimisés :

- Pas de hot-reload
- Mode production pour Next.js
- Images minimales
- Health checks configurés

## Commandes Make disponibles

```bash
make docker-build      # Build les images Docker
make docker-up         # Démarre les conteneurs
make docker-down       # Arrête les conteneurs
make docker-logs       # Affiche les logs
make docker-deploy     # Build + démarre (tout-en-un)
```

## Bonnes pratiques

1. **Ne pas commit les secrets** : Utilisez des variables d'environnement
2. **Volumes pour les données** : Les données persistantes sont montées comme volumes
3. **Logs** : Utilisez `docker-compose logs -f` pour déboguer
4. **Health checks** : Les services ont des health checks configurés
5. **Networks** : Les services communiquent via un réseau Docker dédié
