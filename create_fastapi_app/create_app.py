
import os
from create_fastapi_app.templates import install_template
from create_fastapi_app.helpers.git import try_git_init

def create_app(app_path: str):
    root = os.path.abspath(app_path)
    app_name = os.path.basename(root)
    # Create the directory if it doesn't exist
    os.makedirs(root, exist_ok=True)
    print(f"Creating a new Fastapi app in [bold green]{root}[/bold green].")

    # Change the current working directory to the specified root
    os.chdir(root)
    install_template(app_name, root)

    git = try_git_init(root)
    print("git", git)
    if git:
        print("Initialized a git repository.")   
         