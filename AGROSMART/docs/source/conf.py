import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'AgroSmart'
copyright = '2025'
author = 'Guilherme Mota 2022144\nDiogo'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
]

html_theme = 'sphinx_rtd_theme'
language = 'pt_BR'