_Creating and deploying a new package version is easy_

### Prerequisites

1. Ensure you're on the latest `master` branch

2. Ensure you have access to a PyPI account that is a maintainer of [scaleapi](https://pypi.org/project/scaleapi/) on PyPI

### Deployment Steps:

**Step 0: Critical - Bump Project Version**

Ensure `_version.py` has an updated project version. If not, please increment the project version, commit and push the changes.

We use [semantic versioning](https://packaging.python.org/guides/distributing-packages-using-setuptools/#semantic-versioning-preferred). If you are adding a meaningful feature, bump the minor version. If you are fixing a bug, bump the incremental version.

**Step 1: Run Publish Script**

```
./publish.sh
```

If you want to run test cases via `pytest` before publishing, add the _optional_ `runtest` arg to the script.

You need to set your own test key as `SCALE_TEST_API_KEY` environment variable before running.
```
SCALE_TEST_API_KEY="{apikey}|{userid}|test" ./publish.sh runtest
```

**Step 2: Check out the PyPI page to ensure all looks good**

[https://pypi.org/project/scaleapi/](https://pypi.org/project/scaleapi/)

**Step 3: Create a New Release**

Create a [new release](https://github.com/scaleapi/scaleapi-python-client/releases/new) on GitHub with a matching version tag _(i.e. v2.0.1)_. Please provide a summary about new features and fixed bugs in the Release Notes.
