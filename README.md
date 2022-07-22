# Harpia Project

Harpia é um instalador feito em python
Foca principalmente em repositórios do Github

![Python Ver](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)


## Install

Using PIP command:

```shell
git clone https://github.com/LunarPyOrg/harpia # Will clone 'main' branch
cd harpia
pip install .
```

Build and install (install poetry with `pip install poetry` first):

```shell
git clone https://github.com/LunarPyOrg/harpia # Will clone 'main' branch
cd harpia
poetry build
pip install dist/harpia-*.whl
```

### Uninstall

```shell
pip uninstall harpia
```


## Contribute

You'll need to use [poetry](https://github.com/python-poetry/poetry) dependencie manager:

```shell
git clone --branch dev https://github.com/LunarPyOrg/harpia
cd harpia

# To run main() function from harpia/main.py
poetry run harpia

# To build to a .whl file
poetry build

# To install the build file using pip
pip install dist/harpia-APPVERSION-PYTHONVERSION-none-any.whl
```
