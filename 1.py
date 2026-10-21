
from pathlib import Path

# Root directory for the project
ROOT = Path(".")

# Project directory structure
directories = [
    "alembic/versions",
    "app/models",
    "app/schemas",
    "app/api",
    "app/services",
    "app/agents",
    "app/utils",
    "tests",
]

# Project files
files = [
    ".env.example",
    ".gitignore",
    "Dockerfile",
    "docker-compose.yml",
    "README.md",
    "requirements.txt",
    "alembic.ini",

    "alembic/env.py",

    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/database.py",

    "app/models/__init__.py",
    "app/models/user.py",
    "app/models/document.py",

    "app/schemas/__init__.py",
    "app/schemas/user.py",
    "app/schemas/document.py",

    "app/api/__init__.py",
    "app/api/auth.py",
    "app/api/documents.py",
    "app/api/chat.py",
    "app/api/analytics.py",

    "app/services/auth_service.py",
    "app/services/ingestion_service.py",
    "app/services/embedding_service.py",
    "app/services/rag_service.py",
    "app/services/agent_service.py",
    "app/services/ml_service.py",

    "app/agents/__init__.py",
    "app/agents/state.py",
    "app/agents/nodes.py",
    "app/agents/graph.py",

    "app/utils/__init__.py",
    "app/utils/security.py",
    "app/utils/logger.py",

    "tests/__init__.py",
    "tests/test_auth.py",
    "tests/test_documents.py",
    "tests/test_rag.py",
]


def create_project():
    # Create directories
    for directory in directories:
        path = ROOT / directory
        path.mkdir(parents=True, exist_ok=True)
        print(f"[DIR]  {path}")

    # Create files without overwriting existing files
    for filename in files:
        path = ROOT / filename
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.touch()
            print(f"[FILE] {path}")
        else:
            print(f"[SKIP] {path} already exists")

    print("\nProject structure created successfully!")


if __name__ == "__main__":
    create_project()
