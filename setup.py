import os
from setuptools import setup


def get_readme_content():
    return open(os.path.join(os.path.dirname(__file__), 'README.md')).read()


setup(
    name = 'aio-geojson-query',
    version = '0.0.1',
    description = 'Something something geojson',
    author = 'Chris F Ravenscroft',
    author_email = 'chris@voilaweb.com',
    url = 'https://github.com/Fusion/pywhistle',
    license = 'MIT',
    long_description = get_readme_content(),
    packages = ['aio_geojson_query',],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    install_requires = [
        'aiodns', 'aiohttp>=3.5.4',
        'aio_geojson_client>=0.13',
        'pytz>=2019.01'
        ],
)