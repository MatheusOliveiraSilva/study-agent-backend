.PHONY: install lint format test check

# Use uv for environment management and running commands
UV = uv

# Default target: runs lint and tests
check: lint test

# Install dependencies (including optional/dev)
install:
	$(UV) pip install -r pyproject.toml --all-extras # Adjust --all-extras if needed

# Run linters
lint:
	@echo "Running ruff linter..."
	$(UV) run ruff check .
	@echo "Checking ruff formatting..."
	$(UV) run ruff format --check .

# Apply automatic formatting
format:
	@echo "Applying ruff formatting..."
	$(UV) run ruff format .

# Run tests
test:
	@echo "Running pytest..."
	$(UV) run pytest 