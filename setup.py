import sys

if sys.version_info < (3, 0):
    sys.exit(
        ("This doesn't support python 2,"
         " it doesn't support {0}").format(sys.version))

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

setup(name='kaggler',
      version='2018.08.28',
      description=("Code for a practice kaggle competition."),
      author="russell",
      platforms=['linux'],
      url='https://github.com/necromuralist/kaggle-competitions',
      author_email="cloisteredmonkey.jmark@slmail.me",
      packages=find_packages(),
      )
