import sys
import warnings

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
        'contact us at support@scaleapi.com.',
        DeprecationWarning)
    install_requires.append('pyOpenSSL')
    install_requires.append('ndg-httpsclient')
    install_requires.append('pyasn1')
    install_requires.append('idna')
    install_requires.append('requests[security]')

setup(
    name = 'scaleapi',
    packages = ['scaleapi'],
    version = '0.3.1',
    description = 'The official Python client library for the Scale API, the API for human intelligence.',
    author = 'Calvin Huang',
    author_email = 'c@lvin.me',
    url = 'https://github.com/scaleapi/scaleapi-python-client',
    keywords = ['scale', 'scaleapi', 'humans', 'tasks', 'categorization', 'transcription', 'annotation', 'comparison', 'data collection', 'audio transcription'],
    install_requires = install_requires,
    classifiers = ['Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5',
                   'License :: OSI Approved :: MIT License',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries']
)
