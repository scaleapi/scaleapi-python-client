import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = ["requests>=2.25.0", "urllib3>=1.26.0"]


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
    packages=["scaleapi"],
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
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
)
