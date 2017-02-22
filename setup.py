from distutils.core import setup

setup(
  name = 'metadata-extractor',
  packages = ['metadata_extractor'],
  package_dir = {'metadata_extractor': 'metadata_extractor'},
  package_data = {'metadata_extractor': ['__init__.py']},
  version = '0.5',
  description = 'Extract metadatas from unstructured and semi-structured sources',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/metadata-extractor',
  download_url = 'https://github.com/DanielJDufour/metadata-extractor/tarball/download',
  keywords = ['metadata','geo','python','tagging'],
  classifiers = [],
)
