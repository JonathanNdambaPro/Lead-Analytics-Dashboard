# Installation

Ce guide vous explique comment installer et configurer l'environnement de développement.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.13+** : [Télécharger Python](https://www.python.org/downloads/)
- **Node.js 20+** : [Télécharger Node.js](https://nodejs.org/)
- **pnpm** : `npm install -g pnpm` ou `corepack enable`
- **uv** : `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Docker & Docker Compose** (optionnel) : [Installer Docker](https://docs.docker.com/get-docker/)

## Installation du Backend

### 1. Cloner le repository

```bash
git clone https://github.com/JonathanNdambaPro/Lead-Analytics-Dashboard.git
cd Lead-Analytics-Dashboard
```

### 2. Installer les dépendances Python

```bash
# Installation avec uv (rapide)
make install

# Ou manuellement
uv sync
uv run pre-commit install
```

Cette commande va :

- Créer un environnement virtuel `.venv`
- Installer toutes les dépendances Python
- Configurer les pre-commit hooks

### 3. Vérifier l'installation

```bash
# Vérifier que Python et les dépendances sont bien installés
uv run python --version
uv run uvicorn --version
```

## Installation du Frontend

### 1. Naviguer vers le dossier frontend

```bash
cd frontend
```

### 2. Installer les dépendances Node.js

```bash
# Avec pnpm (recommandé)
pnpm install

# Ou avec npm
npm install
```

### 3. Vérifier l'installation

```bash
# Vérifier que Next.js est bien installé
pnpm next --version
```

## Installation avec Docker

Si vous préférez utiliser Docker :

```bash
# Build des images
make docker-build

# Démarrage des conteneurs
make docker-up
```

## Structure des fichiers après installation

```
Lead-Analytics-Dashboard/
├── .venv/                    # Environnement virtuel Python
├── backend/
│   ├── __pycache__/
│   └── ...
├── frontend/
│   ├── node_modules/        # Dépendances Node.js
│   ├── .next/              # Build Next.js (après pnpm dev)
│   └── ...
└── uv.lock                  # Lock file des dépendances Python
```

## Commandes utiles

```bash
# Vérifier la qualité du code
make check

# Lancer les tests
make test

# Mettre à jour les dépendances
uv sync

# Backend
cd backend && uv run uvicorn backend.app:app --reload

# Frontend
cd frontend && pnpm dev
```

## Troubleshooting

### Erreur : `uv: command not found`

Assurez-vous que uv est bien installé et dans votre PATH :

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # ou ~/.zshrc
```

### Erreur : `pnpm: command not found`

Installez pnpm globalement :

```bash
npm install -g pnpm
# ou
corepack enable
```

### Erreur de permissions Python

Si vous rencontrez des erreurs de permissions, utilisez uv qui gère automatiquement l'environnement virtuel :

```bash
uv sync --reinstall
```

## Prochaines étapes

- [Configuration](configuration.md) : Configurer les variables d'environnement
- [Docker](docker.md) : Utiliser Docker pour le développement
