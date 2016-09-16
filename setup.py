from setuptools import setup, find_packages
# noinspection PyPep8Naming
from setuptools.command.test import test as TestCommand
from setuptools import Command
from subprocess import call
from codecs import open
import os
import sys

if sys.version_info.major < 3:
    sys.exit('Python 2 is not supported')


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


class PyTestCov(Command):
    description = "run tests and report them to codeclimate"
    user_options= []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = call(["py.test", "--cov=pyCardDeck", "--durations=10", "tests"], shell=True)
        if os.getenv("TRAVIS_PULL_REQUEST") == "false":
            call(["codeclimate-test-reporter", "--file", ".coverage"], shell=True)
        raise SystemExit(errno)


test_requirements = ['pytest>=3.0.1', 'pytest-cov>=2.3.1', 'codeclimate-test-reporter>=0.1.2']

requirements = ['PyYAML>=3.11', 'jsonpickle>=0.9.3']
if sys.version_info.minor < 5:
    requirements.append('typing>=3.5.2.2')

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyCardDeck',
      version='1.2.0',
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
      install_requires=requirements,
      cmdclass={'test': PyTest, 'testcov': PyTestCov},
      tests_require=test_requirements
      )
