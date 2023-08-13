import typer
import time
from rich import print
from enum import Enum
import questionary
from rich.progress import Progress, SpinnerColumn, TextColumn

class NeuralNetwork(str, Enum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"
        
app = typer.Typer()

disabled_message: str = "Unavailable at this time"
data = {
    "name": "Rick",
    "age": 42,
    "items": [{"name": "Portal Gun"}, {"name": "Plumbus"}],
    "active": True,
    "affiliation": None,
}

@app.command()
def create_project(    
):
    """
    This create a fastapi project.
    """
    answers = questionary.form(
        project_name = questionary.text("What is your project named?", default="my_app"),
        sonarqube = questionary.confirm("Would you like to use SonarQube?", default=False),
        relationship_database = questionary.select("Choose a relationship database", choices=["PostgreSQL", questionary.Choice("SQLite", disabled=disabled_message), questionary.Choice("MySQL", disabled=disabled_message)]),
        athentication_integration = questionary.select("Choose the authentication service", choices=["default", questionary.Choice("Cognito", disabled=disabled_message)]),
        #athentication_integration = questionary.select("Choose the authentication service", choices=["No (or I'll add it later)",  questionary.Separator(), "item2", questionary.Choice("item3", disabled=disabled_message),]),
        third = questionary.checkbox('Select toppings', choices=["Cheese", "Tomato", "Pineapple"])
    ).ask()
    questionary.print(f"Hello World 🦄, {answers}", style="bold italic fg:darkred")
    #print("answers", answers)
    
    confirmation = questionary.confirm("Are you sure you want to create the project it?").ask()

    if not confirmation:
        print("Not created")
        raise typer.Abort()
    print("Creating project!")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:        
        progress.add_task(description="Creating...", total=None)
        time.sleep(5)
    print("Done!")    
    
    # Add your project generation logic here


if __name__ == "__main__":
    app()
