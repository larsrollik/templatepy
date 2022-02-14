[![DOI](https://zenodo.org/badge/370470893.svg)](https://zenodo.org/badge/latestdoi/370470893)

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
