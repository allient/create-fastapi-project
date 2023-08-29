import os
import re
import typer
import questionary
from rich import print
from questionary import Validator, ValidationError
from rich.progress import Progress, SpinnerColumn, TextColumn
from create_fastapi_project.create_app import create_app
from create_fastapi_project.templates import ITemplate
from rich.panel import Panel
from rich.console import Console

console = Console()
app = typer.Typer()

disabled_message: str = "Unavailable at this time"


class ProjectNameValidator(Validator):
    def validate(self, document):
        pattern = r"^[a-zA-Z_][\w-]*$"
        if not re.match(pattern, document.text):
            raise ValidationError(
                message="Project name should start with a letter or underscore and consist of letters, numbers, or underscores. For example: backend",
                cursor_position=len(document.text),
            )


@app.command()
def create_project():
    """
    This create a fastapi project.
    """
    project_name: str = questionary.text(
        "What is your project named?",
        validate=ProjectNameValidator,
        default="backend",
    ).ask()
    basic = ITemplate.basic.value
    langchain_basic = ITemplate.langchain_basic.value
    full = ITemplate.full.value
    template_type: str = questionary.select(
        "Choose a template",
        choices=[basic, langchain_basic, full],
    ).ask()
    if template_type == ITemplate.full:
        questionary.select(
            "Choose the authentication service",
            choices=[
                "default",
                questionary.Choice("cognito", disabled=disabled_message),
            ],
        ).ask()
        questionary.select(
            "Choose a relationship database",
            choices=[
                "PostgreSQL",
                questionary.Choice("SQLite", disabled=disabled_message),
                questionary.Choice("MySQL", disabled=disabled_message),
            ],
        ).ask()
        (
            questionary.checkbox(
                "Select toppings", choices=["Cheese", "Tomato", "Pineapple"]
            )
            .skip_if(project_name != "", default=[])
            .ask()
        )

    # is_packages_installation_required: bool = questionary.confirm(
    #     "Would you like to install poetry packages?", default=False
    # ).ask()

    message = f"You are going to create a project named '{project_name}' using the '{template_type}' template."
    styled_message = console.render_str(f"[bold italic fg=dark_red]🐍 {message}[/]")
    panel = Panel(styled_message, title="Project Initialization")
    console.print(panel)

    confirmation: bool = questionary.confirm("Are you sure you want to continue?").ask()
    if not confirmation:
        print("Not created")
        raise typer.Abort()
    print("Creating project!")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Creating project...", total=None)

        project_path: str = project_name.strip()
        resolved_project_path = os.path.abspath(project_path)

        """
        Verify the project dir is empty or doesn't exist
        """
        # Resolve the absolute path of the project
        root = os.path.abspath(resolved_project_path)
        # Check if the folder exists
        folder_exists = os.path.exists(root)

        if folder_exists and os.listdir(root):
            print("There is already a project with same name created")
            raise typer.Abort()

        """
        Check if the directory is writable
        """
        if not os.access(os.path.dirname(root), os.W_OK):
            print(
                "The application path is not writable, please check folder permissions and try again."
            )
            print("It is likely you do not have write permissions for this folder.")
            raise typer.Abort()

        create_app(resolved_project_path, template=template_type)


if __name__ == "__main__":
    app()
