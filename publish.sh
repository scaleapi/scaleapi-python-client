#!/bin/bash
echo "##### STARTING BUILD and PUBLISH #####"

VERSION_FILE="scaleapi/_version.py"

staged_files=$(git diff --cached --name-only --diff-filter=ACMR ${VERSION_FILE})
changed_files=$(git diff --name-only --diff-filter=ACMR ${VERSION_FILE})

if [[ "$staged_files" == "$VERSION_FILE" ||  "$changed_files" == "$VERSION_FILE" ]];
then
    echo "ERROR: You have uncommitted changes in version file: ${VERSION_FILE}"
    echo "       Please commit and push your changes before publishing."
    exit
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "${DIR}" || exit 1

BRANCH_NAME=$(git branch 2>/dev/null | grep '^*' | tr -d ' *')
echo "Active Git Branch: ${BRANCH_NAME}" # release-1.0.5

# IFS='-' read -ra strarr <<< "$BRANCH_NAME"
# BRANCH_PREFIX="${strarr[0]}"  # release
# BRANCH_VERSION="${strarr[1]}" # 1.0.5

while IFS= read -r line; do
    if [[ $line == __version__* ]];
    then
        IFS=' = ' read -ra strarr <<< "$line"
        PKG_VERSION=$( sed -e 's/^"//' -e 's/"$//' <<< "${strarr[1]}" )
        echo "SDK Package Version: ${PKG_VERSION}"
        break
    fi
done < "${DIR}/${VERSION_FILE}"

if [ "$BRANCH_NAME" != "master" ];
then
    echo "ERROR: You need to be in 'master' git branch to publish this version (${PKG_VERSION})."
    exit 1
fi

if [ "$1" == "runtest" ];
then
    echo "Validating environment for pytest..."
    if ! pip show pytest > /dev/null 2>&1;
    then
        echo "WARN: 'pytest' package is not found, installing...";
        pip install pytest
    fi

    if [[ -z "${SCALE_TEST_API_KEY}" ]]; then
        echo "Test key not found. Please assign 'SCALE_TEST_API_KEY=...' as your test environment key."
        exit 1
    fi

    if ! python -m pytest; then echo "ERROR: pytest failed."; exit; fi
    echo "pytest is successful!"
fi

# Clean-up build and dist folders
rm -rf build/ dist/

# Build package
echo "Building package..."

if ! python3 setup.py sdist bdist_wheel > /dev/null 2>&1; then echo "ERROR: Package building failed."; exit 1; fi


if ! pip show twine > /dev/null 2>&1;
then
    echo "WARN: 'twine' package is not found, installing...";
    pip install twine
fi

# Twine Validation
echo "Validating package..."

if ! twine check --strict dist/* ; then echo "ERROR: Twine check failed."; exit 1; fi

# Twine Upload to Pypi
echo "Uploading package..."

if ! twine upload dist/*; then echo "ERROR: Twine upload failed."; exit 1; fi

exit 0;
