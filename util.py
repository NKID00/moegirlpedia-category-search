__version__ = '0.2.0'

from pathlib import Path

from httpx import __version__ as httpx_version

ROOT_DIR = Path('cache/')
USER_AGENT = (
    f'moegirlpedia-category-search/{__version__}'
    f' (https://github.com/NKID00/moegirlpedia-category-search)'
    f' httpx/{httpx_version}'
)
PROXY = None
