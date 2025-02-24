import os.path

from setuptools import find_packages, setup

install_requires = [
    "requests>=2.25.0",
    "urllib3>=1.26.0",
    "python_dateutil>=2.8.2",
    "pydantic>=2",
    "typing-extensions>=4.7.1",
]


def read(rel_path):
    """Read lines from given file"""
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    """Read __version__ from given file"""
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError(f"Unable to find a valid __version__ string in {rel_path}.")


setup(
    name="scaleapi",
    packages=find_packages(),
    version=get_version("scaleapi/_version.py"),
    description="The official Python client library for Scale AI, "
    "the Data Platform for AI",
    author="Scale AI",
    author_email="support@scale.com",
    url="https://github.com/scaleapi/scaleapi-python-client",
    keywords=[
        "scale",
        "scaleapi",
        "tasks",
        "categorization",
        "labeling",
        "annotation",
    ],
    install_requires=install_requires,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
)
