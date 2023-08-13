import os
from create_fastapi_app.templates import ITemplate, install_template
from create_fastapi_app.helpers.git import try_git_init
from create_fastapi_app.helpers.install import add_configuration_to_pyproject, create_poetry_project, install_dependencies
from rich import print


def create_app(app_path: str, template: ITemplate = ITemplate.basic):
    root = os.path.abspath(app_path)
    app_name = os.path.basename(root)
    # Create the directory if it doesn't exist
    os.makedirs(root, exist_ok=True)
    print(f"Creating a new Fastapi app in [bold green]{root}[/bold green].")

    # Change the current working directory to the specified root
    os.chdir(root)
    has_pyproject = install_template(root, template, app_name)
    

    if try_git_init(root):
        print("Initialized a git repository.")

    # Compare paths and assign cdpath
    original_directory: str = os.getcwd()
    cdpath: str = app_path
    if os.path.join(original_directory, app_name) == app_path:
        cdpath = app_name

    print(f"[bold green]Success![/bold green] Created {app_name} at {app_path}.")

    if has_pyproject:
        print("Inside that directory, you can run several commands:\n")
        # print(f"[cyan]  make {'yarn' if use_yarn else 'run'} dev[/cyan]")
        print("    Starts the development server.\n")
        print("[cyan]  make run-dev-build[/cyan]")
        print("    Builds the app for production.\n")
        print("[cyan]  make run-prod[/cyan]")
        print("    Runs the built app in production mode.\n")
        print("We suggest that you begin by typing:\n")
        print(f"[cyan]  cd {cdpath}[/cyan]")
