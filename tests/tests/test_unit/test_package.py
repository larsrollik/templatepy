# import os
import subprocess

import pytest


@pytest.fixture(scope="module")
def install_package():
    # Install the package in a temporary environment
    subprocess.run(["pip", "install", "."], check=True)
    yield
    # Cleanup (optional)
    subprocess.run(["pip", "uninstall", "-y", "templatepy"], check=True)


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
    # Bump version major
    result = subprocess.run(
        ["bump2version", "major", "--dry-run"], capture_output=True, text=True
    )

    # Ensure that no commit happens (dry-run should not make any commits)
    assert "Committed" not in result.stdout, "Version bump made a commit"

    # Check that the version file would be bumped
    # (check for expected version change in the output)
    assert "bumped version" in result.stdout, "Version bump did not happen"

    # Check the version in `__init__.py` or version file to see if it's changed
    with open("templatepy/__init__.py", "r") as f:
        version = f.read()
        assert (
            "0.0.4" in version
        )  # Example, this should match the bumped version.


def test_bump_version_minor(install_package):
    # Bump version minor
    result = subprocess.run(
        ["bump2version", "minor", "--dry-run"], capture_output=True, text=True
    )

    # Ensure no commit happens
    assert "Committed" not in result.stdout, "Version bump made a commit"

    # Check for expected version change
    assert "bumped version" in result.stdout, "Version bump did not happen"

    # Optionally, check the version in `__init__.py`
    with open("templatepy/__init__.py", "r") as f:
        version = f.read()
        assert "0.1.0" in version  # Example, match expected version


def test_bump_version_patch(install_package):
    # Bump version patch
    result = subprocess.run(
        ["bump2version", "patch", "--dry-run"], capture_output=True, text=True
    )

    # Ensure no commit happens
    assert "Committed" not in result.stdout, "Version bump made a commit"

    # Check for expected version change
    assert "bumped version" in result.stdout, "Version bump did not happen"

    # Optionally, check the version in `__init__.py`
    with open("templatepy/__init__.py", "r") as f:
        version = f.read()
        assert "0.0.4" in version  # Example, match expected version


if __name__ == "__main__":
    pytest.main()
