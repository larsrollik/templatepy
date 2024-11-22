import subprocess

import pytest


# Predefined bump2version flags for easy modification
BUMPER_FLAGS = ["--no-commit", "--no-tag"]


@pytest.fixture(scope="module")
def install_package():
    # Install the package in a temporary environment
    subprocess.run(["pip", "install", "."], check=True)
    yield
    # Cleanup (optional)
    subprocess.run(["pip", "uninstall", "-y", "templatepy"], check=True)


def get_current_version():
    # Get the current version from `__init__.py` or the version file
    with open("templatepy/__init__.py", "r") as f:
        version = f.read()
    return version.split("__version__ = '")[1].split("'")[0]


def test_pre_commit_hooks(install_package):
    # Run pre-commit hooks (without making changes to the main repo)
    result = subprocess.run(
        ["pre-commit", "run", "--all-files"], capture_output=True, text=True
    )

    # Check if the pre-commit hooks ran successfully
    assert (
        result.returncode == 0
    ), f"Pre-commit failed with output: {result.stdout}"


def test_bump_version_release(install_package):
    # Get the current version before the bump
    current_version = get_current_version()

    # Run release version bump
    result = subprocess.run(
        ["bump2version", "release"] + BUMPER_FLAGS,
        capture_output=True,
        text=True,
    )

    # Ensure that no commit or tag happens
    assert "Committed" not in result.stdout, "Version bump made a commit"
    assert "tag" not in result.stdout, "Version bump created a tag"

    # Check that the version file would be bumped
    assert "bumped version" in result.stdout, "Version bump did not happen"

    # Get the version after the bump
    new_version = get_current_version()

    # Ensure the version is different (i.e., it was bumped)
    assert (
        current_version != new_version
    ), f"Version did not bump: {current_version} -> {new_version}"


if __name__ == "__main__":
    pytest.main()
