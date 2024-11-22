import re
import subprocess

import pytest

# Bump2version flags for easy modification
BUMPER_FLAGS = ["--no-commit", "--no-tag"]


@pytest.fixture(scope="module")
def install_package():
    # Install the package in a temporary environment
    subprocess.run(["pip", "install", "."], check=True)
    yield
    # Cleanup (optional)
    subprocess.run(["pip", "uninstall", "-y", "templatepy"], check=True)


def get_current_version():
    """Read the current version from the __init__.py file."""
    with open("templatepy/__init__.py", "r") as f:
        content = f.read()
        # Use regex to get version (assuming it is in a __version__ variable)
        match = re.search(r"__version__ = ['\"]([^'\"]+)['\"]", content)
        if match:
            return match.group(1)
        else:
            raise ValueError("Version not found in templatepy/__init__.py")


def test_pre_commit_hooks(install_package):
    # Run pre-commit hooks (without making changes to the main repo)
    result = subprocess.run(
        ["pre-commit", "run", "--all-files"], capture_output=True, text=True
    )

    # Check if the pre-commit hooks ran successfully
    assert (
        result.returncode == 0
    ), f"Pre-commit failed with output: {result.stdout}"


def test_bump_version_major(install_package):
    # Get the current version before the bump
    current_version = get_current_version()

    # Bump version major (without commit or tag)
    result = subprocess.run(
        ["bump2version", "major"] + BUMPER_FLAGS,
        capture_output=True,
        text=True,
    )

    # Ensure that no commit happens (no commit message in stdout)
    assert "Committed" not in result.stdout, "Version bump made a commit"

    # Ensure no tag is created
    assert "tag" not in result.stdout, "Version bump created a tag"

    # Ensure the version has been bumped (check new version in the output)
    bumped_version = get_current_version()
    assert bumped_version != current_version, "Version bump did not happen"


def test_bump_version_minor(install_package):
    # Get the current version before the bump
    current_version = get_current_version()

    # Bump version minor (without commit or tag)
    result = subprocess.run(
        ["bump2version", "minor"] + BUMPER_FLAGS,
        capture_output=True,
        text=True,
    )

    # Ensure no commit happens
    assert "Committed" not in result.stdout, "Version bump made a commit"

    # Ensure no tag is created
    assert "tag" not in result.stdout, "Version bump created a tag"

    # Ensure the version has been bumped (check the new version in the output)
    bumped_version = get_current_version()
    assert bumped_version != current_version, "Version bump did not happen"


def test_bump_version_patch(install_package):
    # Get the current version before the bump
    current_version = get_current_version()

    # Bump version patch (without commit or tag)
    result = subprocess.run(
        ["bump2version", "patch"] + BUMPER_FLAGS,
        capture_output=True,
        text=True,
    )

    # Ensure no commit happens
    assert "Committed" not in result.stdout, "Version bump made a commit"

    # Ensure no tag is created
    assert "tag" not in result.stdout, "Version bump created a tag"

    # Ensure the version has been bumped (check the new version in the output)
    bumped_version = get_current_version()
    assert bumped_version != current_version, "Version bump did not happen"


if __name__ == "__main__":
    pytest.main()
