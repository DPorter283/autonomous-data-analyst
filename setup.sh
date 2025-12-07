#!/bin/bash

echo "🚀 Initializing Senior-Level Project Structure..."

# 1. Create Directory Structure
mkdir -p .github/workflows docs/architecture infra/terraform notebooks src/{agents,core,tools} tests/{unit,integration,evals}

# 2. Create Empty Python Files
touch src/__init__.py
touch src/agents/__init__.py src/agents/analyst_agent.py src/agents/sql_agent.py
touch src/core/__init__.py src/core/config.py src/core/logger.py
touch src/tools/__init__.py src/tools/database_connector.py src/tools/chart_generator.py
touch src/main.py

touch tests/__init__.py
touch tests/unit/test_sql_generation.py
touch tests/integration/test_aws_connection.py

# 3. Create .gitignore
cat <<EOT >> .gitignore
__pycache__/
*.py[cod]
.env
.venv
env/
venv/
.DS_Store
.idea/
.vscode/
*.ipynb_checkpoints
infra/terraform/.terraform/
infra/terraform/*.tfstate*
EOT

# 4. Create pyproject.toml
cat <<EOT >> pyproject.toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "autonomous-data-analyst"
version = "0.1.0"
description = "A RAG-based agent that queries AWS Redshift via Bedrock"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "langchain>=0.1.0",
    "langgraph>=0.0.10",
    "langchain-aws>=0.1.0",
    "boto3>=1.34.0",
    "pydantic>=2.0.0",
    "pandas>=2.0.0",
    "fastapi>=0.109.0",
    "uvicorn>=0.27.0",
    "aws-lambda-powertools>=2.30.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
    "black>=23.0.0",
    "ipykernel>=6.0.0"
]

[tool.ruff]
line-length = 88
target-version = "py311"
EOT

# 5. Create Makefile
cat <<EOT >> Makefile
.PHONY: install test lint format run

install:
	pip install -e .[dev]

test:
	pytest tests/

lint:
	ruff check src/

format:
	black src/

run:
	python src/main.py
EOT

# 6. Create README.md
cat <<EOT >> README.md
# Autonomous Data Analyst Agent (ADAA)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![AWS](https://img.shields.io/badge/cloud-AWS-orange)

## 📖 Project Overview
The **Autonomous Data Analyst Agent (ADAA)** is a secure, retrieval-augmented generation (RAG) system deployed on AWS.

## 🏗 Architecture
* **Orchestration:** \`LangGraph\`
* **LLM Backend:** \`AWS Bedrock\` (Claude 3.5 Sonnet)
* **Data Warehouse:** \`AWS Redshift\`
* **Infrastructure:** \`Terraform\`

## 🚀 Getting Started
\`\`\`bash
make install
make test
\`\`\`
EOT

# 7. Git Init
git add .
git commit -m "feat: initial project structure with senior-level architecture"

echo "✅ Setup Complete!"
