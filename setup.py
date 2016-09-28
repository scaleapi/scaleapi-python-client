from distutils.core import setup
setup(
    name = 'scaleapi',
    packages = ['scaleapi'],
    version = '0.1',
    description = 'A client library for interacting with the Scale API',
    author = 'Calvin Huang',
    author_email = 'c@lvin.me',
    url = 'https://github.com/scaleapi/scale-api-python-client',
    download_url = 'https://github.com/scaleapi/scale-api-python-client/tarball/0.1',
    keywords = ['scale', 'scaleapi'],
    install_requires = ['requests', 'enum34'],
    classifiers = [],
)
