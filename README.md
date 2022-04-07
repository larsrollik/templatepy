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

[//]: # (Badges)

[![DOI](https://zenodo.org/badge/370470893.svg)](https://zenodo.org/badge/latestdoi/370470893)
[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fgithub.com/larsrollik/templatepy)](https://github.com/larsrollik/templatepy)
[![PyPI](https://img.shields.io/pypi/v/templatepy.svg)](https://pypi.org/project/templatepy)
[![Wheel](https://img.shields.io/pypi/wheel/templatepy.svg)](https://pypi.org/project/templatepy)
![CI](https://github.com/larsrollik/templatepy/workflows/tests/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)


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

#### General
- `LICENSE`: license text

- `README.md`: [Github-flavored markdown] file

- `templatepy`: placeholder folder for any python package that is configured for install via `setup.cfg` and `pyproject.toml`
  - `__init__.py`: contains basic package info and example function that is called by console entrypoint (see `setup.cfg`)
  - `example.data.file.config`: a file to demonstrate that data files are included based on `setup.cfg` criteria
  - `example.data.file.test-extension-yu48`: a file to demonstrate data exclusion via `setup.py`

#### Packaging system
  - `MANIFEST.in`: [manifest] file describes included/excluded files for build

  - `pyproject.toml`:
    - specifies build system: this replaces the usual `setup.py` architecture for setuptools
    - config for [black] code formatter

  - `setup.cfg`:
    - package specification and install dependencies
    - config for [bump2version] and `flake8` formatting (see pre-commit)

  - `setup.py`: legacy file (see notes on new build-system below)

#### Code maintenance (linting/formatting/github)
- `.pre-commit-config.yaml`: use [pre-commit] to run code formatting (e.g. with [black] and `flake8`) and PEP compliance checks
  - Install pre-commit hook with `pre-commit install` (Note: only installs it in the current virtual environment)
  - Run it manually with `pre-commit run --all` or leave it to run on commit (requires to re-stage changed files!)

- `.github`: folder that contains github automation workflows and issues templates

- `.gitignore`: ignored files/folders in git tools



## TODO for **adapting** template to new project

- [ ] Change package name:
  - (1) `templatepy` folder
  - (2) README.md
  - (3) `name` argument in `setup.cfg`
  - (4) `.github/workflows` files
  - (5) `setup.cfg`: `[bumpversion:file:templatepy/__init__.py]`
- [ ] Change details about project author, etc. in `setup.cfg`, `README.md`, and `templatepy/__init__.py`
- [ ] Change license holder in `LICENSE`
- [ ] Change `README` badge paths at top
- [ ] Verify inclusions/exclusions of installable files/folders in `MANIFEST.in` and `setup.cfg`
- [ ] Check `.gitignore` contains relevant criteria
- [ ] Add all version string locations to `setup.cfg`/bump2version field.
  - Use same syntax as for `[bumpversion:file:PACKAGEFOLDER/__init__.py]` line to describe how to find version on version increment
- [ ] To upload to [pypi]: see below for workflow
- [ ] To upload to [Zenodo] if repo is a publication:
  - (1) Connect Zenodo to Github account
  - (2) Flip switch on zenodo view of repo - **NOTE**: Zenodo can only copy from **public** repos
  - (3) Create new release version of github repo (manual or via `.github/workflows/CI.yaml`)
  - (4) Wait! Zenodo view with DOI assignment should update within about a minute
  - (5) Add DOI badge to `README` file



## Workflow for (automatically) uploading package to [pypi] or [test.pypi]
- (1) On [pypi], make new API key for repo or general
- (2) On [Github](https://github.com/larsrollik/templatepy/settings/secrets/actions/new), in repository settings add a new **actions secret** named `TWINE_API_KEY` and copy in the pypi API key
- (3) Create a new [release](https://github.com/larsrollik/templatepy/releases/new) manually on github or by triggering the github workflow with a version without release extension (e.g. `x.y.z`)



## Notes

#### New(er) build system with `pyproject.toml` and `setup.cfg`
- `pip`
  - tested with `pip install .  --use-feature=in-tree-build` for forward-compatibility with `pip 21.3`
  - keeping empty `setup.py` for enabling install in editable mode `-e` as this still requires such a file
  - added `wheel` as build-system dependency for compatibility with pip that does not implement `PEP 517`
- `setup.cfg`/`setup.py` might be fully replaced with `pyproject.toml`. [See this discussion.](https://stackoverflow.com/questions/44878600/is-setup-cfg-deprecated)

## License
This software is released under the **[BSD 3-Clause License](https://github.com/larsrollik/templatepy/blob/main/LICENSE)**
