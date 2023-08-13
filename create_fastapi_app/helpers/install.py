import subprocess


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
