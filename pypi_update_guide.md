_Creating and deploying a new package version is easy_

### Prerequisites

1. Ensure you're on the latest master

2. Ensure you have a PyPI account created and are added as a Collaborator

### Deployment Steps:

**Step 0: Critical - Bump Project Version**

In `setup.py`, you need to specify a new project version.

We use [semantic versioning](https://packaging.python.org/guides/distributing-packages-using-setuptools/#semantic-versioning-preferred). If you are adding a meaningful feature, bump the minor version. If you are fixing a bug, bump the incremental version.

**Step 1: Remove Previous Versions**

Clear out any previously packages and files in the `dist` and `build/lib` folders

**Step 2: Create a Source Distribution**

```
python3 setup.py sdist
```

**Step 3: Create `wheel`**

You should also create a wheel for your project. A wheel is a built package that can be installed without needing to go through the “build” process. Installing wheels is substantially faster for the end user than installing from a source distribution

```
python3 setup.py bdist_wheel
```

**Step 4: Install Twine**

Twine is what is used to manage PyPI pacakges

```
pip3 install twine
```

**Step 5: Upload distribution to PyPI**

```
twine upload dist/*
```

**Step 6: Check out the PyPI page to ensure all looks good**

[https://pypi.org/project/scaleapi/](https://pypi.org/project/scaleapi/)
