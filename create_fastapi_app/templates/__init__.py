import os
import shutil


def install_template(app_name: str, root: str):
    template = "basic"
    print(f"Initializing project with template: {template}")
    # Get the directory of the current script
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_script_dir, template)

    eslint = False
    # Define the files and subdirectories to copy
    copy_source: list[str] = ["**"]
    ignore: list[str] = []
    if not eslint:
        ignore.append("eslintrc.json")

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

    print("template_path", template_path)
