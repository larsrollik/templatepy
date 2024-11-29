import os
import subprocess

import toml


def get_package_name():
    """Retrieve package name from pyproject.toml."""
    project_data = toml.load("pyproject.toml")
    return project_data["project"]["name"]


def test_python_version():
    """Test that Python version is compatible with the environment."""
    assert os.sys.version_info >= (
        3,
        8,
    ), "Python version must be 3.8 or higher"


def test_package_installation():
    """Test dynamic installation and uninstallation of the package."""
    package_name = get_package_name()

    # Install the package
    subprocess.run(["pip", "install", "."], check=True)

    # Check that the package is installed
    result = subprocess.run(
        ["pip", "show", package_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0, "Package installation failed"

    # Uninstall the package
    subprocess.run(["pip", "uninstall", "-y", package_name], check=True)

    # Verify the package is uninstalled
    result = subprocess.run(
        ["pip", "show", package_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode != 0, "Package uninstallation failed"
