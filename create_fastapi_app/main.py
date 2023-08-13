import os
import re
import typer
import time
import questionary
from rich import print
from questionary import Validator, ValidationError, prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from create_fastapi_app.templates import install_template

app = typer.Typer()

disabled_message: str = "Unavailable at this time"

class ProjectNameValidator(Validator):
    def validate(self, document):
        pattern = r'^[a-zA-Z_][\w-]*$'
        if not re.match(pattern, document.text):
            raise ValidationError(
                message="Project name should start with a letter or underscore and consist of letters, numbers, or underscores. For example: my_app",
                cursor_position=len(document.text),
            )


def create_app(app_path: str):
    root = os.path.abspath(app_path)
    app_name = os.path.basename(root)
    # Create the directory if it doesn't exist
    os.makedirs(root, exist_ok=True)
    print(f"Creating a new Fastapi app in [bold green]{root}[/bold green].")

    # Change the current working directory to the specified root
    os.chdir(root)
    install_template(app_name, root)
    



@app.command()
def create_project(
    project_name: str = questionary.text(
        "What is your project named?",
        validate=ProjectNameValidator,
        default="my_app",
    ).ask(),
    # athentication_integration: str = questionary.select("Choose the authentication service", choices=["default", questionary.Choice("Cognito", disabled=disabled_message)]).ask(),
    # sonarqube: bool = questionary.confirm("Would you like to use SonarQube?", default=False).ask(),
    # relationship_database: str = questionary.select("Choose a relationship database", choices=["PostgreSQL", questionary.Choice("SQLite", disabled=disabled_message), questionary.Choice("MySQL", disabled=disabled_message)]).ask(),
    # third: str = questionary.checkbox('Select toppings', choices=["Cheese", "Tomato", "Pineapple"]).ask()
):
    """
    This create a fastapi project.
    """
    questionary.print(f"Hello World 🦄, {project_name}", style="bold italic fg:darkred")
    confirmation = questionary.confirm(
        "Are you sure you want to create the project it?"
    ).ask()
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
            print("The application path is not writable, please check folder permissions and try again.")
            print("It is likely you do not have write permissions for this folder.")
            raise typer.Abort()

        create_app(resolved_project_path)

        time.sleep(2)
    print("Done!")

    # Add your project generation logic here


if __name__ == "__main__":
    app()
