import subprocess
import sys


def test_python_version() -> None:
    """Test that Python version is compatible with the environment."""
    assert sys.version_info >= (3, 8), "Python version must be 3.8 or higher"


def test_package_installation() -> None:
    """Test dynamic installation and uninstallation of the package."""
    import toml

    package_name = toml.load("pyproject.toml")["project"]["name"]
    package_name = package_name.replace("-", "_")

    # Install the package
    subprocess.run(["uv", "pip", "install", "."], check=True)

    # Check that the package is installed
    result = subprocess.run(
        ["uv", "pip", "show", package_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "Package installation failed"

    # Uninstall the package
    subprocess.run(["uv", "pip", "uninstall", "-y", package_name], check=True)

    # Verify the package is uninstalled
    result = subprocess.run(
        ["uv", "pip", "show", package_name],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, "Package uninstallation failed"
