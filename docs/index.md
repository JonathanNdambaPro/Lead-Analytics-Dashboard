# Lead Analytics Dashboard

[![Release](https://img.shields.io/github/v/release/jojodataascode/dataascode)](https://img.shields.io/github/v/release/jojodataascode/dataascode)
[![Build status](https://img.shields.io/github/actions/workflow/status/jojodataascode/dataascode/main.yml?branch=main)](https://github.com/jojodataascode/dataascode/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/jojodataascode/dataascode)](https://img.shields.io/github/commit-activity/m/jojodataascode/dataascode)
[![License](https://img.shields.io/github/license/jojodataascode/dataascode)](https://img.shields.io/github/license/jojodataascode/dataascode)

Bienvenue dans la documentation du **Lead Analytics Dashboard**, une application complète d'analyse de leads avec un dashboard moderne.

## 🎯 Vue d'ensemble

Lead Analytics Dashboard est une application full-stack permettant de suivre et analyser les événements commerciaux :

- 📞 Prises de contact
- 📅 Appels bookés et proposés
- 🔄 Relances
- 💬 Réponses prospects

## 🏗️ Architecture

### Backend
- **FastAPI** : Framework web moderne et performant
- **DuckDB** : Moteur SQL analytique pour les agrégations
- **Delta Lake** : Format de stockage de données versionné et optimisé
- **Python 3.13** : Dernière version stable de Python
- **uv** : Gestionnaire de dépendances ultra-rapide

### Frontend
- **Next.js 16** : Framework React avec App Router
- **React 19** : Dernière version de React
- **Tailwind CSS** : Framework CSS utility-first
- **Recharts** : Bibliothèque de graphiques pour React
- **shadcn/ui** : Composants UI modernes et accessibles

## ✨ Fonctionnalités principales

### Visualisation des données
- 📊 Graphiques interactifs des événements par semaine et par mois
- 📈 Tableaux de suivi des objectifs
- 🔄 Analyse des ratios de conversion
- 📱 Interface responsive et moderne

### Analyse temporelle
- Agrégations hebdomadaires avec `DATE_TRUNC`
- Agrégations mensuelles
- Unpivot des colonnes de dates pour analyse multi-événements
- Requêtes SQL optimisées avec DuckDB

### Architecture technique
- API REST avec documentation OpenAPI automatique
- Gestion sécurisée des secrets (pas d'ARG Docker)
- Build multi-stage optimisé
- Health checks configurés
- Hot-reload en développement

## 🚀 Démarrage rapide

!!! tip "Deux options disponibles"
    Vous pouvez lancer l'application en développement local ou via Docker.

### Option 1 : Docker (Recommandé)

```bash
# Créer le fichier .env
cat > .env << EOF
NOTION_TOKEN=votre_token
DATABASE_ID=votre_database_id
EOF

# Build et démarrage
make docker-deploy
```

### Option 2 : Développement local

```bash
# Backend
make install
uv run uvicorn backend.app:app --reload

# Frontend (nouveau terminal)
cd frontend && pnpm install && pnpm dev
```

## 📚 Documentation

- [Guide d'installation](getting-started/installation.md)
- [Configuration](getting-started/configuration.md)
- [Docker](getting-started/docker.md)
- [API Backend](api/overview.md)
- [Architecture](architecture.md)

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez le [guide de contribution](https://github.com/jojodataascode/dataascode/blob/main/CONTRIBUTING.md) pour plus d'informations.

## 📝 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](https://github.com/jojodataascode/dataascode/blob/main/LICENSE) pour plus de détails.
