from setuptools import setup, find_packages
# noinspection PyPep8Naming
from setuptools.command.test import test as TestCommand
from codecs import open
import sys


# noinspection PyCallByClass,PyAttributeOutsideInit
class PyTest(TestCommand):
    user_options = [('pytest-args', 'a', 'Arguments to pass into py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


test_requirements = ['pytest>=2.8.0', 'pytest-cov']

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyCardDeck',
      version='1.1.1.0',
      description='Logic for decks with cards',
      long_description=long_description,
      url='https://www.djetelina.cz/project/pycarddeck/',
      author='David Jetelina',
      author_email='david@djetelina.cz',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ],
      keywords='cards deck card game shuffle draw discard',
      packages=find_packages(exclude=['tests', 'docs', 'examples']),
      install_requires=[
          'PyYAML',
      ],
      cmdclass={'test': PyTest},
      tests_require=test_requirements
      )
