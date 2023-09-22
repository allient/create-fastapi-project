import os
import shutil
from enum import Enum
from dotenv import dotenv_values
from create_fastapi_project.helpers.install import (
    add_configuration_to_pyproject,
    install_dependencies,
)


class ITemplate(str, Enum):
    basic = "basic"
    langchain_basic = "langchain_basic"
    full = "full"


def install_template(root: str, template: ITemplate, app_name: str):
    print(f"Initializing project with template: {template}")
    # Get the directory of the current script
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_script_dir, template)

    eslint = False
    # Define the files and subdirectories to copy
    ignore: list[str] = []
    if not eslint:
        ignore.append(".env")

    # Copy files and subdirectories
    shutil.copytree(
        template_path,
        root,
        symlinks=False,
        ignore=shutil.ignore_patterns(*ignore),
        copy_function=shutil.copy2,
        ignore_dangling_symlinks=True,
        dirs_exist_ok=True,
    )

    poetry_path = ""
    if template == ITemplate.full or template == ITemplate.langchain_basic:
        # TODO: CHECK PATHS IN MACOS AND WINDOWS | (os.path.join)        
        poetry_frontend_path = os.path.join(root, "frontend", "app")

    else:
        poetry_path = os.path.join(root, "backend", "app")

    has_pyproject = add_configuration_to_pyproject(poetry_path)

    if has_pyproject:
        dependencies = [
            "fastapi[all]",
            "fastapi-pagination[sqlalchemy]@^0.12.7",
            "asyncer@^0.0.2",
            "httpx@^0.24.1",
        ]
        dev_dependencies = [
            "pytest@^7.4.0",
            "mypy@^1.5.0",
            "ruff@^0.0.284",
            "black@^23.7.0",
        ]
        if template == ITemplate.langchain_basic:
            langchain_dependencies = [
                "langchain@^0.0.265",
                "openai@^0.27.8",
                "adaptive-cards-py@^0.0.7",
                "google-search-results@^2.4.2",
            ]
            frontend_dependencies = [
                "streamlit",
                "websockets",
            ]
            dependencies[0] = "fastapi[all]@^0.99.1"
            dependencies.extend(langchain_dependencies)
        if template == ITemplate.full:
            full_dependencies = [
                "alembic@^1.10.2",
                "asyncpg@^0.27.0",
                "sqlmodel@^0.0.8",
                "python-jose@^3.3.0",
                "cryptography@^38.0.3",
                "passlib@^1.7.4",
                "SQLAlchemy-Utils@^0.38.3",
                "SQLAlchemy@^1.4.40",
                "minio@^7.1.13",
                "Pillow@^9.4.0",
                "watchfiles@^0.18.1",
                "asyncer@^0.0.2",
                "httpx@^0.23.1",
                "pandas@^1.5.3",
                "openpyxl@^3.0.10",
                "redis@^4.5.1",
                "fastapi-async-sqlalchemy@^0.3.12",
                "oso@^0.26.4",
                "celery@^5.2.7",
                "transformers@^4.28.1",
                "requests@^2.29.0",
                "wheel@^0.40.0",
                "setuptools@^67.7.2",
                "langchain@^0.0.262",
                "openai@^0.27.5",
                "celery-sqlalchemy-scheduler@^0.3.0",
                "psycopg2-binary@^2.9.5",
                "fastapi-limiter@^0.1.5 ",
                "fastapi-pagination[sqlalchemy]@^0.11.4 ",
                "fastapi-cache2[redis]@^0.2.1 ",
            ]
            full_dev_dependencies = [
                "pytest-asyncio@^0.21.1",
            ]
            dependencies[0] = "fastapi[all]@^0.95.2"
            dependencies.extend(full_dependencies)
            dev_dependencies.extend(full_dev_dependencies)

        print("- Installing main packages. This might take a couple of minutes.")
        install_dependencies(poetry_path, dependencies)
        print("- Installing development packages. This might take a couple of minutes.")
        install_dependencies(poetry_path, dev_dependencies, dev=True)

        if template == ITemplate.langchain_basic:
            add_configuration_to_pyproject(poetry_frontend_path)
            print(
                "- Installing frontend packages. This might take a couple of minutes."
            )
            install_dependencies(poetry_frontend_path, frontend_dependencies)

        # Set your dynamic environment variables

        # Load variables from .env.example
        example_env = dotenv_values(".env.example")
        example_env["PROJECT_NAME"] = app_name

        # Write modified environment variables to .env and .env.example file
        with open(".env", "w") as env_file, open(
            ".env.example", "w"
        ) as example_env_file:
            for key, value in example_env.items():
                env_file.write(f"{key}={value}\n")
                example_env_file.write(f"{key}={value}\n")

    return has_pyproject
