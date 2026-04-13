import os
import sys

sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
]

source_suffix = '.rst'
master_doc = 'index'

project = 'pyCardDeck'
copyright = '2016-2026, David Jetelina'
author = 'David Jetelina'

version = '1.4'
release = '1.4.0'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = 'pyCardDeckdoc'

latex_documents = [
    (master_doc, 'pyCardDeck.tex', 'pyCardDeck Documentation',
     'David Jetelina', 'manual'),
]

man_pages = [
    (master_doc, 'pycarddeck', 'pyCardDeck Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'pyCardDeck', 'pyCardDeck Documentation',
     author, 'pyCardDeck', 'One line description of project.',
     'Miscellaneous'),
]
