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


def get_current_version(quote_char='"'):
    # Get the current version from `__init__.py` or the version file
    with open("templatepy/__init__.py", "r") as f:
        version = f.read()

    # Use the provided quote character to extract the version
    version_str = version.split(f"__version__ = {quote_char}")[1].split(
        quote_char
    )[0]
    return version_str


def reset_version():
    # Ensure the repository is clean before resetting
    status_result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    if status_result.stdout.strip():
        raise RuntimeError(
            "Repository has uncommitted changes. "
            "Please commit or discard them before resetting."
        )

    # Reset the version by checking out the latest git commit
    subprocess.run(
        ["git", "checkout", "--", "templatepy/__init__.py"], check=True
    )
    subprocess.run(["git", "checkout", "--", "pyproject.toml"], check=True)
    subprocess.run(["git", "checkout", "--", ".bumpversion.cfg"], check=True)
    subprocess.run(["git", "checkout", "--", "README.md"], check=True)


def test_pre_commit_hooks(install_package):
    # Run pre-commit hooks (without making changes to the main repo)
    result = subprocess.run(
        ["pre-commit", "run", "--all-files"], capture_output=True, text=True
    )

    # Check if the pre-commit hooks ran successfully
    assert (
        result.returncode == 0
    ), f"Pre-commit failed with output: {result.stdout}"


def test_bump_version_minor(install_package):
    # Get the current version before the bump
    current_version = get_current_version()

    # Run minor version bump
    result = subprocess.run(
        ["bump2version", "minor"] + BUMPER_FLAGS,
        capture_output=True,
        text=True,
    )

    # Ensure that no commit or tag happens
    assert "Committed" not in result.stdout, "Version bump made a commit"
    assert "tag" not in result.stdout, "Version bump created a tag"

    # Get the version after the bump
    new_version = get_current_version()

    # Check if the version is different
    assert (
        current_version != new_version
    ), f"Version did not bump: {current_version} -> {new_version}"

    # Ensure the new version contains 'dev' or 'rc' after a minor bump
    assert (
        "dev" in new_version or "rc" in new_version
    ), "Version should contain 'dev' or 'rc'"

    # Check if the new version follows the correct format (major.minor.patch)
    assert new_version.count(".") == 2 or (
        new_version.count(".") == 3
        and ("dev" in new_version or "rc" in new_version)
    ), f"New version {new_version} is not in 'major.minor.patch' format"

    reset_version()


def test_bump_version_major(install_package):
    # Get the current version before the bump
    current_version = get_current_version()

    # Run major version bump
    result = subprocess.run(
        ["bump2version", "major"] + BUMPER_FLAGS,
        capture_output=True,
        text=True,
    )

    # Ensure that no commit or tag happens
    assert "Committed" not in result.stdout, "Version bump made a commit"
    assert "tag" not in result.stdout, "Version bump created a tag"

    # Get the version after the bump
    new_version = get_current_version()

    # Ensure the version is different (i.e., it was bumped)
    assert (
        current_version != new_version
    ), f"Version did not bump: {current_version} -> {new_version}"

    # Ensure that the new version contains dev/rc at the end
    assert (
        "dev" in new_version or "rc" in new_version
    ), f"Version {new_version} should contain 'dev' or 'rc'"

    # Ensure that the new version is in the major.minor.patch.dev format
    assert new_version.count(".") == 2 or (
        new_version.count(".") == 3
        and ("dev" in new_version or "rc" in new_version)
    ), f"New version {new_version} is not in the expected format"

    reset_version()


def test_bump_version_release(install_package):
    # Get the current version before the bump
    current_version = get_current_version()

    # Skip the release bump if the current version is already stable
    # (no 'dev' or 'rc')
    if "dev" not in current_version and "rc" not in current_version:
        pytest.skip(
            f"Version {current_version} is already stable, skipping test."
        )

    # Run release version bump
    result = subprocess.run(
        ["bump2version", "release"] + BUMPER_FLAGS,
        capture_output=True,
        text=True,
    )

    # Ensure that no commit or tag happens
    assert "Committed" not in result.stdout, "Version bump made a commit"
    assert "tag" not in result.stdout, "Version bump created a tag"

    # Get the version after the bump
    new_version = get_current_version()

    assert (
        new_version.count(".") == 2
    ), f"Version {new_version} should be in 'major.minor.patch' format"

    assert (
        current_version != new_version
    ), f"Version did not bump: {current_version} -> {new_version}"

    reset_version()


if __name__ == "__main__":
    pytest.main()
