import codecs
import os
import re

from setuptools import setup, find_packages

##################################################################

NAME = 'auacm'
PACKAGES = find_packages(where='src')
META_PATH = os.path.join('src', 'auacm', '__init__.py')
KEYWORDS = ['competitive', 'icpc', 'auacm', 'auburn']
CLASSIFIERS = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.4'
]
INSTALL_REQUIRES = ['requests']

##################################################################

HERE = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    """
    Build an absolute file path from *parts* and return the contents
    of the resulting file. Assume UTF-8 encoding
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as fil:
        return fil.read()

META_FILE = read(META_PATH)

def find_meta(meta):
    """Extract __*meta*__ from META_FILE"""
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string.'.format(meta=meta))

if __name__ == '__main__':
    setup(
        name=NAME,
        description=find_meta('description'),
        license=find_meta('license'),
        url=find_meta('uri'),
        download_url=find_meta('uri') + '/tarball/' + find_meta('version'),
        version=find_meta('version'),
        author=find_meta('author'),
        author_email=find_meta('email'),
        maintainer=find_meta('author'),
        maintainer_email=find_meta('email'),
        keywords=KEYWORDS,
        long_description=read('README.md'),
        packages=PACKAGES,
        package_dir={'': 'src'},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
    )
