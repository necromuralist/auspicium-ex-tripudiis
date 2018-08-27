import sys

if sys.version_info < (3, 0):
    sys.exit(
        ("This doesn't support python 2 ({})".format(sys.version)))

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

setup(name='kaggler',
      version='2018.08.26',
      description=("Code to explore kaggle with."),
      author="russell",
      platforms=['linux'],
      url='https://github.com/necromuralist/kaggle-competitions/',
      author_email="necromuralist@protonmail.com",
      packages=find_packages(),
      )
