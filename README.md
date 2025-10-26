# 📊 Lead Analytics Dashboard

[![Release](https://img.shields.io/github/v/release/jojodataascode/dataascode)](https://img.shields.io/github/v/release/jojodataascode/dataascode)
[![Build status](https://img.shields.io/github/actions/workflow/status/jojodataascode/dataascode/main.yml?branch=main)](https://github.com/jojodataascode/dataascode/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/jojodataascode/dataascode/branch/main/graph/badge.svg)](https://codecov.io/gh/jojodataascode/dataascode)
[![Commit activity](https://img.shields.io/github/commit-activity/m/jojodataascode/dataascode)](https://img.shields.io/github/commit-activity/m/jojodataascode/dataascode)
[![License](https://img.shields.io/github/license/jojodataascode/dataascode)](https://img.shields.io/github/license/jojodataascode/dataascode)

Application d'analyse de leads avec un dashboard moderne permettant de suivre les événements commerciaux (prises de contact, appels, relances, réponses prospects) avec des agrégations par semaine et par mois.

## 🏗️ Architecture

- **Backend** : FastAPI + DuckDB + Delta Lake (Python 3.13)
- **Frontend** : Next.js 16 + React 19 + Tailwind CSS + Recharts
- **Gestion de dépendances** : uv (backend) + pnpm (frontend)
- **Déploiement** : Docker + Docker Compose

## 📋 Liens

- **Github repository**: <https://github.com/jojodataascode/dataascode/>
- **Documentation** : <https://jojodataascode.github.io/dataascode/>
- **Documentation Docker** : [DOCKER.md](DOCKER.md)

## ✨ Fonctionnalités

- 📈 **Visualisation des événements** : Graphiques interactifs des événements par semaine et mois
- 📊 **Tableaux d'objectifs** : Suivi des objectifs hebdomadaires et mensuels
- 🔄 **Ratios de conversion** : Analyse des taux de conversion entre les différentes étapes
- 🎯 **Agrégations temporelles** : Analyses par semaine et par mois via DuckDB
- 💾 **Stockage Delta Lake** : Format de données optimisé et versionné
- ☁️ **Google Cloud Storage** : Stockage cloud distribué et durable pour Delta Lake
- 🔐 **Sécurité** : Gestion sécurisée des secrets (pas d'ARG Docker pour les données sensibles)

## 🚀 Démarrage rapide

### Prérequis

- Python 3.13+
- Node.js 20+
- Docker & Docker Compose (pour le déploiement containerisé)
- pnpm (pour le frontend)
- uv (pour le backend)

### Option 1 : Développement local

#### Backend

```bash
# Installation des dépendances Python
make install

# Lancer le backend
make deploy_local
# ou directement :
uv run uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

Le backend sera accessible sur <http://localhost:8000>
Documentation API : <http://localhost:8000/docs>

#### Frontend

```bash
cd frontend

# Installation des dépendances
pnpm install

# Lancer le frontend
pnpm dev
```

Le frontend sera accessible sur <http://localhost:3000>

### Option 2 : Déploiement Docker (Recommandé)

```bash
# Créer un fichier .env à la racine
cat > .env << EOF
NOTION_TOKEN=votre_token_ici
DATABASE_ID=votre_database_id_ici
GCS_URI=gs://notion-dataascode/data_leads
EOF

# Placer vos credentials GCS (si vous utilisez GCS)
cp /chemin/vers/credentials.json ./gcs-credentials.json

# Build et démarrage
make docker-deploy

# Ou manuellement :
make docker-build
make docker-up
```

**Services disponibles** :
- Frontend : <http://localhost:3000>
- Backend API : <http://localhost:8000>
- Documentation API : <http://localhost:8000/docs>

Pour plus de détails sur Docker, consultez [DOCKER.md](DOCKER.md).

## 📁 Structure du projet

```
dataascode/
├── backend/                    # Backend FastAPI
│   ├── app.py                 # Point d'entrée FastAPI
│   ├── core/                  # Configuration et modèles OpenAPI
│   ├── data_leads/            # Données Delta Lake
│   └── routers/               # Routes API
│       ├── ingestion_leads/   # Ingestion des données
│       └── transformation/    # Transformations et agrégations
├── frontend/                   # Frontend Next.js
│   ├── src/
│   │   ├── app/              # Pages Next.js
│   │   ├── components/       # Composants React
│   │   └── lib/              # Utilitaires et API client
│   └── public/               # Assets statiques
├── Dockerfile.backend          # Image Docker backend
├── Dockerfile.frontend         # Image Docker frontend
├── docker-compose.yml          # Orchestration des services
├── Makefile                    # Commandes de développement
└── pyproject.toml             # Configuration Python & dépendances
```

## 🛠️ Développement

### Installation de l'environnement

```bash
# Installation avec pre-commit hooks
make install

# Vérifier le code
make check

# Lancer les tests
make test
```

### Pre-commit hooks

Avant chaque commit, les hooks vérifient :
- Formatage du code (black, ruff)
- Linting (ruff, mypy)
- Sécurité (detect-secrets, bandit)
- Qualité SQL (sqlfluff)
- Validation Docker

Pour lancer manuellement :

```bash
uv run pre-commit run -a
```

## 📚 Documentation

- **API Backend** : <http://localhost:8000/docs> (Swagger/OpenAPI)
- **Docker** : [DOCKER.md](DOCKER.md)
- **Contribution** : [CONTRIBUTING.md](CONTRIBUTING.md)
- **Documentation MkDocs** : `make docs`

## 🧪 Tests et qualité

```bash
# Lancer les tests
make test

# Vérifier la qualité du code
make check

# Build la documentation
make docs-test
```

## 🐳 Commandes Docker utiles

```bash
# Build des images
make docker-build

# Démarrer les conteneurs
make docker-up

# Arrêter les conteneurs
make docker-down

# Voir les logs
make docker-logs

# Tout en un (build + start)
make docker-deploy
```

## 🔐 Variables d'environnement

Le projet utilise des variables d'environnement pour la configuration. Créez un fichier `.env` à la racine :

```bash
# Backend - Notion Integration
NOTION_TOKEN=secret_xxxxxxxxxxxxx
DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Google Cloud Storage (pour production)
GCS_URI=gs://notion-dataascode/data_leads
# Le fichier gcs-credentials.json doit être à la racine (pour Docker)

# Frontend - API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

⚠️ **Important** :
- Ne committez jamais le fichier `.env` avec des vraies valeurs
- Ne committez jamais les fichiers `*credentials*.json`
- Les données sensibles sont passées via des variables d'environnement, **jamais** via `ARG` dans les Dockerfiles

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines.

### Workflow de contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'feat: add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence [LICENSE](LICENSE).

## 📞 Support

Pour toute question ou problème :
- Ouvrir une [issue](https://github.com/jojodataascode/dataascode/issues)
- Consulter la [documentation](https://jojodataascode.github.io/dataascode/)

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
