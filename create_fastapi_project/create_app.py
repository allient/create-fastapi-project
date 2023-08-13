import os
from create_fastapi_project.templates import ITemplate, install_template
from create_fastapi_project.helpers.git import try_git_init
from rich import print
from rich.panel import Panel
from rich.console import Console

console = Console()

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

    if has_pyproject:
        success_message = f"[bold green]🚀 Success![/bold green] Created {app_name} at {app_path}."
        instructions = f"""
        [bold cyan]Inside that directory, you can run several commands:[/bold cyan]

        • [cyan]make install[/cyan] - Make sure packages are installed.
        • [cyan]make run-dev-build[/cyan] or [cyan]make run-app[/cyan] - Starts the development server.
        • [cyan]make run-prod[/cyan] - Builds and runs the app in production mode.

        We suggest that you begin by typing:
        [cyan]cd {cdpath}[/cyan]
        """

        styled_success_message = console.render_str(success_message)
        styled_instructions = console.render_str(instructions)

        success_panel = Panel(styled_success_message, title="🎉 Project Created", style="bold green")
        instructions_panel = Panel(styled_instructions, title="🛠️ Get Started", style="bold cyan")

        print(success_panel)
        print(instructions_panel)
