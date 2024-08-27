# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../ttv_battleroyale'))

project = 'Battle Royale Twitch Chat Bot'
copyright = '2024, Héctor Rodríguez (hecrp)'
author = 'Héctor Rodríguez (hecrp)'
release = '0.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add any additional configuration to resolve import issues
autodoc_mock_imports = ['twitchio']
