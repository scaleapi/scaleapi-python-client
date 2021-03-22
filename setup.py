import sys
import warnings
import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = ['requests>=2.4.2']

if sys.version_info < (3, 4, 0):
    install_requires.append('enum34')

if sys.version_info < (2, 7, 9):
    warnings.warn(
        'Users have reported issues with SNI / SSL by using Scale on '
        'versions of Python older than 2.7.9. If at all possible, you should '
        'upgrade your version of Python. '
        'If you have any questions, please file an issue on Github or '
        'contact us at support@scale.com.',
        DeprecationWarning)
    install_requires.append('pyOpenSSL')
    install_requires.append('ndg-httpsclient')
    install_requires.append('pyasn1')
    install_requires.append('idna')
    install_requires.append('requests[security]')

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find a valid __version__ string in %s." % rel_path)

setup(
    name='scaleapi',
    packages=['scaleapi'],
    version=get_version("scaleapi/_version.py"),
    description='The official Python client library for Scale AI, the Data Platform for AI',
    author='Scale AI',
    author_email='support@scale.com',
    url='https://github.com/scaleapi/scaleapi-python-client',
    keywords=[
        'scale',
        'scaleapi',
        'tasks',
        'categorization',
        'labeling',
        'annotation',
    ],
    install_requires=install_requires,
    classifiers=['Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: 3.10',
                 'License :: OSI Approved :: MIT License',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Libraries']
)
