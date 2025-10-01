.PHONY: help install install-dev test lint format type-check security clean run

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Emotiv LSL - Development Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install package and dependencies
	@echo "$(BLUE)Installing package...$(NC)"
	pip install -e .

install-dev: ## Install package with development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	pip install -e ".[dev,analysis]"
	pip install pre-commit
	pre-commit install

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	pytest tests/ -v --cov=emotiv_lsl --cov-report=term-missing

test-fast: ## Run tests without coverage
	@echo "$(BLUE)Running fast tests...$(NC)"
	pytest tests/ -v

lint: ## Run linters
	@echo "$(BLUE)Running linters...$(NC)"
	flake8 emotiv_lsl/ tests/ examples/
	pylint emotiv_lsl/

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(NC)"
	black emotiv_lsl/ tests/ examples/ *.py
	isort emotiv_lsl/ tests/ examples/ *.py

type-check: ## Run type checker
	@echo "$(BLUE)Running type checker...$(NC)"
	mypy emotiv_lsl/ --ignore-missing-imports

security: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	bandit -r emotiv_lsl/ -ll
	safety check -r requirements.txt

quality: lint type-check security ## Run all quality checks

pre-commit: ## Run pre-commit hooks on all files
	@echo "$(BLUE)Running pre-commit hooks...$(NC)"
	pre-commit run --all-files

clean: ## Clean build artifacts
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .tox/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-data: ## Clean data files (BE CAREFUL!)
	@echo "$(YELLOW)Warning: This will delete all data files!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -f data/json/*.json; \
		rm -f data/fif/*.fif; \
		rm -f data/plots/*.png; \
		rm -f data/plots/*.json; \
		echo "$(GREEN)Data files cleaned$(NC)"; \
	fi

run: ## Run the LSL server
	@echo "$(BLUE)Starting LSL server...$(NC)"
	python main.py

run-debug: ## Run the LSL server with debug logging
	@echo "$(BLUE)Starting LSL server (debug mode)...$(NC)"
	python main.py --log-level DEBUG

run-streamlit: ## Run the Streamlit app
	@echo "$(BLUE)Starting Streamlit app...$(NC)"
	streamlit run streamlit_app.py

docs: ## Build documentation (placeholder for future)
	@echo "$(YELLOW)Documentation build not yet implemented$(NC)"

deps-check: ## Check for dependency updates
	@echo "$(BLUE)Checking for outdated dependencies...$(NC)"
	pip list --outdated

deps-update: ## Update dependencies (interactive)
	@echo "$(YELLOW)This will update all dependencies. Continue?$(NC)"
	@read -p "Press Enter to continue or Ctrl+C to cancel..."
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

setup: install-dev ## Complete development setup
	@echo "$(GREEN)Development environment ready!$(NC)"

ci: format lint type-check security test ## Run CI checks locally
	@echo "$(GREEN)All CI checks passed!$(NC)"

