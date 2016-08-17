from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyCardDeck',
      version='1.0.0.dev1',
      description='Logic for decks with cards',
      long_description=long_description,
      url='',
      author='David Jetelina',
      author_email='david@djetelina.cz',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5'
      ],
      keywords='cards deck card game shuffle draw discard',
      packages=find_packages(exclude=['tests', 'docs']),
      install_requires=[]
      )
