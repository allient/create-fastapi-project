import os
import shutil
from enum import Enum
from dotenv import dotenv_values
from create_fastapi_project.helpers.install import add_configuration_to_pyproject, install_dependencies

class ITemplate(str, Enum):
    basic = "basic"
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


    # Add pyproject.toml file and installl packages
    app_folder: str = "app"
    if template == ITemplate.full:
        app_folder = "backend/app"
    
    poetry_path = os.path.join(root, app_folder)
    has_pyproject = add_configuration_to_pyproject(poetry_path)

    if has_pyproject:
        dependencies = ["fastapi[all]", "fastapi-pagination[sqlalchemy]@^0.12.7", "asyncer@^0.0.2", "httpx@^0.24.1"]
        dev_dependencies = ["pytest@^5.2", "mypy@^1.5.0", "ruff@^0.0.284", "black@^23.7.0"]
        print("- Installing main packages. This might take a couple of minutes.")
        install_dependencies(poetry_path, dependencies)
        print("- Installing development packages. This might take a couple of minutes.")
        install_dependencies(poetry_path, dev_dependencies, dev=True)
        # Set your dynamic environment variables
        
        # Load variables from .env.example
        example_env = dotenv_values(".env.example")
        example_env["PROJECT_NAME"] = app_name

        # Write modified environment variables to .env and .env.example file
        with open(".env", "w") as env_file, open(".env.example", "w") as example_env_file:
            for key, value in example_env.items():
                env_file.write(f"{key}={value}\n")
                example_env_file.write(f"{key}={value}\n")

    return has_pyproject


