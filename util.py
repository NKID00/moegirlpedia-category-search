__version__ = '0.1.1'

from pathlib import Path

from httpx import __version__ as httpx_version

root_dir = Path('cache/')
user_agent = (
    f'moegirlpedia-category-search/{__version__}'
    f' (https://github.com/NKID00/moegirlpedia-category-search)'
    f' httpx/{httpx_version}'
)
