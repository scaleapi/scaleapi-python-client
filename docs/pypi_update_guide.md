# Deployment and Publishing Guide for Python SDK

_Creating and deploying a new package version is easy!_

### Prerequisites

1. Ensure you're on the latest `master` branch

2. Ensure the master already has an incremented version

3. *(Required if you are manually publishing to PyPI)* Ensure you have access to a PyPI account that is a maintainer of [scaleapi](https://pypi.org/project/scaleapi/) on PyPI

**How to Bump Project Version**

Ensure `_version.py` has an updated project version. If not, please increment the project version, commit and push the changes.

We use [semantic versioning](https://packaging.python.org/guides/distributing-packages-using-setuptools/#semantic-versioning-preferred). If you are adding a meaningful feature, bump the minor version. If you are fixing a bug, bump the incremental version.
### Deployment:


#### Automated Deployment and Publish with CircleCI:

Our repo already has a publish worklow built into the CircleCI. It's trigerred when there's a new release on GitHub, with a specific version tag.

In order to deploy and publish a new version:
- Create a new [Release](https://github.com/scaleapi/scaleapi-python-client/releases) on GitHub
- Create and assign a new tag in the release page with the following template: `vX.Y.Z` Please make sure `X.Y.Z` is matching the version in the `_version.py`.
  - *i.e.* If the version in `_version.py` is **2.3.1** then the tag should be **v2.3.1**
- Provide release notes by following the [Release Notes Template](release_notes_template.md) and filling relevant sections to your changes.
#### *(Unpreferred)* Manual Deployment and Publish:


**Step 1: Run Publish Script**

```bash
./publish.sh
```

If you want to run test cases via `pytest` before publishing, add the _optional_ `runtest` arg to the script.

You need to set your own test key as `SCALE_TEST_API_KEY` environment variable before running.

```bash
SCALE_TEST_API_KEY="{apikey}|{userid}|test" ./publish.sh runtest
```

**Step 2: Check out the PyPI page to ensure all looks good**

[https://pypi.org/project/scaleapi/](https://pypi.org/project/scaleapi/)

**Step 3: Create a New Release**

Create a [new release](https://github.com/scaleapi/scaleapi-python-client/releases/new) on GitHub with a matching version tag _(i.e. v2.0.1)_. Provide release notes by following the [Release Notes Template](release_notes_template.md) and filling relevant sections to your changes.
