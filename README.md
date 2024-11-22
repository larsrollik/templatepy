[//]: # (Links)
[Github-flavored markdown]: https://github.github.com/gfm

[manifest]: https://packaging.python.org/en/latest/guides/using-manifest-in
[packaging]: https://packaging.python.org/en/latest/tutorials/packaging-projects
[setup.cfg]: https://setuptools.pypa.io/en/latest/userguide/declarative_config.html

[bump2version]: (https://github.com/c4urself/bump2version
[pre-commit]: https://pre-commit.com
[black]: https://github.com/psf/black

[pypi]: pypi.org
[test.pypi]: test.pypi.org

[Zenodo]: https://zenodo.org

[contribution guidelines]: https://github.com/larsrollik/templatepy/blob/main/CONTRIBUTING.md
[issues]: https://github.com/larsrollik/templatepy/issues
[BSD 3-Clause License]: https://github.com/larsrollik/templatepy/blob/main/LICENSE
[Github]: https://github.com/larsrollik/templatepy/settings/secrets/actions/new
[release]: https://github.com/larsrollik/templatepy/releases/new

[//]: # (Badges)

[![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](https://github.com/larsrollik/templatepy/blob/main/CONTRIBUTING.md)
[![DOI](https://zenodo.org/badge/370470893.svg)](https://zenodo.org/badge/latestdoi/370470893)
[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fgithub.com/larsrollik/templatepy)](https://github.com/larsrollik/templatepy)
[![PyPI](https://img.shields.io/pypi/v/templatepy.svg)](https://pypi.org/project/templatepy)
[![Wheel](https://img.shields.io/pypi/wheel/templatepy.svg)](https://pypi.org/project/templatepy)
![CI](https://github.com/larsrollik/templatepy/workflows/tests/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


# templatepy
Template repo for python repositories & PyPi integration
---
**Version: "0.0.3"**


## Usage
1. **Change** files according to overview in `TODO` below
2. **Develop** package...
3. **Install** package:
   - static/normal install: `pip install .`
   - editable install:`pip install -e .`
   - dev install: `pip install -e .[dev]` (some terminals require to escape brackets with ` \ ` as `\[`, esp. zsh)



## File overview


### General
- `LICENSE`: license text

- `README.md`: [Github-flavored markdown] file

- `templatepy`: placeholder folder for any python package that is configured for install via `setup.cfg` and `pyproject.toml`
  - `__init__.py`: contains basic package info and example function that is called by console entrypoint (see `setup.cfg`)
  - `example.data.file.config`: a file to demonstrate that data files are included based on `setup.cfg` criteria
  - `example.data.file.test-extension-yu48`: a file to demonstrate data exclusion via `setup.py`


### Testing
- `tests`: placeholder folder for unit/integration tests and associated data
- `pytest.ini`: config for testing framework with `pytest` and `coverage` plugin (`pytest-cov`)


### Packaging System (see: [packaging] and [pyproject.toml])

- **`MANIFEST.in`**:
  Defines additional files to include/exclude in the build (if not automatically detected).

- **`pyproject.toml`**:
  Central configuration file that replaces the traditional `setup.cfg` and `setup.py` files:
  - **Build System**: Specifies the build system requirements and configuration, as defined in [PEP 518](https://peps.python.org/pep-0518/) and [PEP 621](https://peps.python.org/pep-0621/).
  - **Package Metadata**: Includes the project's metadata (name, version, dependencies, etc.).
  - **Code Formatting**: Configuration for tools like [black] and [flake8] (if used).
  - **Optional Dependencies**: Organizes extra dependencies for development or other environments.

- **`setup.py`**:
  Legacy file retained only for backward compatibility if needed (e.g., older tooling). New projects should avoid it entirely.


## CI Workflow Overview

The CI workflow is triggered on push to `main` or when a tag is created. It ensures code quality and automates the release process:

1. **Linting and Testing**:
   - `lint`: Checks code style with `black` and `flake8`, runs pre-commit hooks.
   - `test`: Runs tests with `pytest` and generates coverage reports.

2. **Tag Validation**:
   - `check-tag`: Verifies that the tag is valid (not `dev` or `rc`) before proceeding.

3. **Release Creation**:
   - `release`: Creates a GitHub release when the tag is valid.

4. **Deployment to PyPI**:
   - `deploy`: Builds and uploads the package to PyPI using `twine`.

The pipeline ensures code quality, passing tests, and automated deployment on new releases.


### Code maintenance (linting/formatting/github)
- `.pre-commit-config.yaml`: use [pre-commit] to run code formatting (e.g. with [black] and `flake8`) and PEP compliance checks
  - Install pre-commit hook with `pre-commit install` (Note: only installs it in the current virtual environment)
  - Run it manually with `pre-commit run --all` or leave it to run on commit (requires to re-stage changed files!)

- `.github`: folder that contains github automation workflows and issues templates

- `.gitignore`: ignored files/folders in git tools

- `.bumpversion.cfg`:  config for [bump2version]

## TODO for **adapting** template to new project

- [ ] Change package name:
  - (1) Rename the `templatepy` folder.
  - (2) Update all occurrences in `README.md`.
  - (3) Update the `name` field in `pyproject.toml`.
  - (4) Update `.github/workflows` files.
  - (5) Update version references in `pyproject.toml` and `templatepy/__init__.py`.
- [ ] Update project author and metadata details in `pyproject.toml`, `README.md`, and `templatepy/__init__.py`.
- [ ] Update the license holder in the `LICENSE` file.
- [ ] Update `README.md` badge paths at the top.
- [ ] Verify inclusions/exclusions of installable files/folders in `MANIFEST.in` and `pyproject.toml` under `[tool.setuptools]`.
- [ ] Ensure `.gitignore` contains relevant entries for the new project.
- [ ] Add all version string locations to `[tool.bump2version]` in `pyproject.toml`.
  - Use syntax like `[bumpversion:file:templatepy/__init__.py]` to specify locations for version updates.
- [ ] To upload to [PyPI], follow the instructions in the section below.
- [ ] To upload to [Zenodo] (if the repository is for a publication):
  - (1) Connect Zenodo to your GitHub account.
  - (2) Enable Zenodo integration for the repository (Zenodo requires the repository to be **public**).
  - (3) Create a new GitHub release (manually or via `.github/workflows/CI.yaml`).
  - (4) Wait for Zenodo to sync and assign a DOI (this usually takes about a minute).
  - (5) Add the DOI badge to `README.md`.


## Workflow for Automatically Uploading Package to [PyPI] or [Test PyPI]

1. **Generate a PyPI API Key**:
   - Go to [PyPI](https://pypi.org/) and create a new API key, either specific to the repository or a general-purpose key.

2. **Add the API Key to GitHub**:
   - In your repository's settings on [GitHub](https://github.com/):
     - Navigate to **Settings > Secrets and variables > Actions**.
     - Add a new **Actions secret** with the name `TWINE_API_KEY`.
     - Paste the PyPI API key into the secret's value field.

3. **Create a New Release**:
   - On [GitHub](https://github.com/), create a new release manually via the **Releases** page.
     - Use a version number without a release extension (e.g., `x.y.z`).
   - Alternatively, trigger the GitHub workflow configured for releasing.

The package will then be automatically uploaded to [PyPI](https://pypi.org/) or [Test PyPI](https://test.pypi.org/) as configured in your CI/CD workflow.


## Notes

#### New(er) Build System with `pyproject.toml` and `setup.cfg`

Historically, packaging in Python was governed by standards such as `PEP-426`, `PEP-517`, and `PEP-518`. These PEPs introduced various mechanisms for packaging and building Python projects, but with certain limitations, especially regarding flexibility and future-proofing.

- **PEP-426**: Introduced the `setup.cfg` and `setup.py` files as the standard way to define package metadata and build configuration.
- **PEP-517**: Introduced a standardized interface for building Python projects, separating the build process from the packaging process and allowing for more flexible build systems.
- **PEP-518**: Defined how `pyproject.toml` should be used to declare build dependencies and system requirements, allowing tools like `pip` to know which backend to use for the build process.

While these PEPs were important milestones, the latest changes to the packaging ecosystem make `pyproject.toml` the preferred way to configure projects going forward.

- **`pip`**:
  - Tested with `pip install . --use-feature=in-tree-build` for forward compatibility with `pip 21.3` and later.
  - While `setup.py` is technically optional, an empty `setup.py` is still kept for enabling editable installs (`pip install -e .`), as this requires such a file for now.
  - `wheel` is added as a build-system dependency to maintain compatibility with versions of `pip` that do not yet fully implement `PEP 517`.

- **Replacing `setup.cfg` and `setup.py` with `pyproject.toml`**:
  - In the modern packaging ecosystem, `pyproject.toml` is increasingly the standard for declaring build systems, dependencies, and metadata. This configuration file simplifies the process and eliminates the need for separate `setup.py` and `setup.cfg` files in many cases.

For further reading on the transition to `pyproject.toml` and the removal of `setup.py`/`setup.cfg`, see the following discussions:
- [PEP-426](https://peps.python.org/pep-0426/)
- [PEP-517](https://peps.python.org/pep-0517/)
- [PEP-518](https://peps.python.org/pep-0518/)
- [Discussion on Setup.cfg Deprecation](https://stackoverflow.com/questions/44878600/is-setup-cfg-deprecated)


## Contributing
Contributions are very welcome!
Please see the [contribution guidelines] or check out the [issues]

## License
This software is released under the **[BSD 3-Clause License]**
