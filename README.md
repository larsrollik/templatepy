[![DOI](https://zenodo.org/badge/370470893.svg)](https://zenodo.org/badge/latestdoi/370470893)
[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fgithub.com/larsrollik/templatepy)](https://github.com/larsrollik/templatepy)
[![PyPI](https://img.shields.io/pypi/v/templatepy.svg)](https://pypi.org/project/templatepy)
[![Wheel](https://img.shields.io/pypi/wheel/templatepy.svg)](https://pypi.org/project/templatepy)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)


# templatepy
Template repo for python repositories & PyPi integration
---


## Usage & file overview

- `setup.py`: to install the package with `pip`, lists dependencies in `install_requires` keyword.
  - Install development version for features below with `pip install -e package[dev]` to select `extras_require` packages as well
- `.pre-commit-config.yaml`: use [pre-commit](https://pre-commit.com) to run code formatting (e.g. with [black](https://github.com/psf/black) and `flake8`) and PEP compliance checks
  - Install pre-commit hook with `pre-commit install` (Note: only installs it in the current virtual environment)
- `.toml`: config for black code formatter (see above)
- `setup.cfg`: config for [bump2version](https://github.com/c4urself/bump2version) and `flake8` formatting (see pre-commit)
- `MANIFEST.in`: description to select included files and directories for installation (see [here](https://packaging.python.org/en/latest/guides/using-manifest-in) for details)
- `LICENSE`: legal info about sharing and using of this code
- `README.md`: markdown readme file
- `.github`: folder that contains github automation workflows and issues templates
  - workflow for linting: install pre-commit hooks locally via `pre-commit install` in the repo dir
  - workflow for uploading package to [pypi](pypi.org): (1) get pypi API key in your account, (2) add new github repo secret for actions at [https://github.com/larsrollik/templatepy/settings/secrets/actions/new](https://github.com/larsrollik/templatepy/settings/secrets/actions/new) as `TWINE_API_KEY`, (3) create new release by tagging a commit with `git tag $TAG_NAME` or on github at [https://github.com/larsrollik/templatepy/releases/new](https://github.com/larsrollik/templatepy/releases/new)
- `.gitignore`: ignored files/folders in git tools
- `package`: placeholder folder for any python package that is configured for install via `setup.py`


## TODO for adapting template to new project

- [ ] Change package name: (1) `package` folder, (2) README.md, (3) `name` argument in `setup.py`, (4) `.github/workflows` files, (5) `setup.cfg`: `[bumpversion:file:PACKAGEFOLDER/__init__.py]`
- [ ] Change details about project author, etc. in `setup.py`, `README.md`, and `package/__init__.py`
- [ ] Change license holder in `LICENSE`
- [ ] Verify inclusions/exclusions of installable files/folders in `MANIFEST.in`
- [ ] Check `.gitignore` contains relevant criteria
- [ ] Add all locations to `setup.cfg` that will contain the version string. Use same syntax as for `[bumpversion:file:PACKAGEFOLDER/__init__.py]` line to describe how to find version on version increment


## License
This software is released under the **[BSD 3-Clause License](https://github.com/larsrollik/templatepy/blob/main/LICENSE)**
