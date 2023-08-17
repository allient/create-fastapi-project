import subprocess
import os
from rich import print
import toml

def create_poetry_project(
    root: str,
    author: str = "Your Name <your@email.com>",
    description: str = "A sample fastapi project created with create-fastapi-project",
) -> bool:
    # Construct the command and arguments
    args = [
        "poetry",
        "init",
        "--name",
        "app",
        "--author",
        author,
        "--description",
        description,
        "--no-interaction",
    ]

    # Run the initialization process
    process = subprocess.Popen(
        args, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error initializing project: {stderr.decode('utf-8')}")

    pyproject_path = os.path.join(root, "pyproject.toml")
    has_pyproject = os.path.exists(pyproject_path)
    return has_pyproject


def install_python_packages(root):
    # Construct the command and arguments
    args = ["poetry", "install"]

    # Run the installation process
    process = subprocess.Popen(
        args, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error installing packages: {stderr.decode('utf-8')}")

    print(stdout.decode("utf-8"))


def install_dependencies(root: str, dependencies: list[str], dev: bool = False):
    # Construct the command and arguments
    args = ["poetry", "add"]
    args.extend(dependencies)
    if dev:
        args.append("-G")
        args.append("dev")

    # Run the installation process
    process = subprocess.Popen(
        args, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error installing dependencies: {stderr.decode('utf-8')}")

    decoded_stdout = stdout.decode("utf-8", errors="replace")
    print(decoded_stdout)


def add_configuration_to_pyproject(
    root: str,
    author: str = "Your Name <your@email.com>",
    description: str = "A sample fastapi project created with create-fastapi-project",
) -> bool:
    config = {
        "tool": {
            "poetry": {
                "name": "app",
                "version": "0.1.0",
                "description": description,
                "authors": [author],
                "readme": "README.md",
                "packages": [{"include": "app"}],
                "dependencies": {
                    "python": ">=3.10,<3.12"
                }
            },
            "black": {
                "line-length": 88,
                "target-version": ["py37", "py38", "py39", "py310", "py311"],
                "exclude": "((.eggs | .git | .pytest_cache | build | dist))",
            },
            "ruff": {
                "line-length": 88,
                "exclude": [".git", "__pycache__", ".mypy_cache", ".pytest_cache"],
                "select": [
                    "E",
                    "W",
                    "F",
                    "C",
                    "B",
                ],
                "ignore": ["B904", "B006", "E501", "B008", "C901"],
                "per-file-ignores": {"__init__.py": ["F401"]},
            },
            "mypy": {
                "warn_return_any": True,
                "warn_unused_configs": True,
                "ignore_missing_imports": True,
                "exclude": ["alembic", "__pycache__"],
            },
            "build-system": {
                "requires": ["poetry-core"],
                "build-backend": "poetry.core.masonry.api",
            },
        }
    }

    pyproject_path = os.path.join(root, "pyproject.toml")

    pyproject = {}
    pyproject.update(config)

    with open(pyproject_path, "w") as file:
        toml.dump(pyproject, file)

    pyproject_path = os.path.join(root, "pyproject.toml")
    has_pyproject = os.path.exists(pyproject_path)
    return has_pyproject
