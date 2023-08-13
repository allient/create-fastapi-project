import subprocess
import os
import shutil


def is_in_git_repository() -> bool:
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.CalledProcessError:
        pass
    return False


def is_in_mercurial_repository() -> bool:
    try:
        subprocess.run(["hg", "root"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        pass
    return False


def is_default_branch_set() -> bool:
    try:
        subprocess.run(
            ["git", "config", "init.defaultBranch"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except Exception:
        pass
    return False


def try_git_init(root: str) -> bool:
    did_init = False
    try:
        subprocess.run(
            ["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if is_in_mercurial_repository() or is_in_git_repository():
            return False

        subprocess.run(["git", "init"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        did_init = True

        if not is_default_branch_set():
            subprocess.run(
                ["git", "checkout", "-b", "main"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        subprocess.run(
            ["git", "add", "-A"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Create Fastapi Project"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except Exception:
        if did_init:
            try:
                shutil.rmtree(os.path.join(root, ".git"), ignore_errors=True)
            except Exception:
                pass
        return False
