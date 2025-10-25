.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync
	@uv run pre-commit install

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@uv run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@uv run deptry .

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: publish
publish: ## Publish a release to PyPI.
	@echo "🚀 Publishing."
	@uvx twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

.PHONY: build-and-publish
build-and-publish: build publish ## Build and publish.

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@uv run mkdocs serve

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.PHONY: deploy_local
deploy_local: ## Launch the application
	@uv run uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload && npm run dev

.PHONY: docker-build
docker-build: ## Build Docker images
	@echo "🐳 Building Docker images"
	@docker-compose build

.PHONY: docker-up
docker-up: ## Start Docker containers
	@echo "🐳 Starting Docker containers"
	@docker-compose up -d

.PHONY: docker-down
docker-down: ## Stop Docker containers
	@echo "🐳 Stopping Docker containers"
	@docker-compose down

.PHONY: docker-logs
docker-logs: ## Show Docker logs
	@echo "🐳 Showing Docker logs"
	@docker-compose logs -f

.PHONY: docker-deploy
docker-deploy: docker-build docker-up ## Build and start Docker containers
	@echo "✅ Application deployed on Docker"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"

.DEFAULT_GOAL := help
