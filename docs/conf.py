# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# read the version from version.txt
with open(os.path.join("../pathfinding3d", "version.txt"), encoding="utf-8") as file_handler:
    __version__ = file_handler.read().strip()


project = "pathfinding3d"
copyright = "2024, Harisankar Babu"
author = "Harisankar Babu"
release = __version__
version = __version__


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # for autodoc
    "sphinx.ext.ifconfig",  # for if statements
    "sphinx.ext.autosummary",  # for autosummary
    "sphinx.ext.doctest",  # for doctest
    "sphinx.ext.todo",  # for todo list
    "sphinx.ext.viewcode",  # for source code
    "sphinx.ext.napoleon",  # for google style docstrings
    "sphinx.ext.githubpages",  # for github pages
    "sphinx.ext.inheritance_diagram",  # for inheritance diagrams
    "sphinx.ext.graphviz",  # for graphviz
    "sphinx.ext.mathjax",  # for math
    "sphinx_autodoc_typehints",  # for type hints
    "sphinx_autodoc_annotation",  # for annotations
    "sphinx_copybutton",  # for copy button
    "sphinx-prompt",  # for prompt
    "notfound.extension",  # for 404 page
    "recommonmark",  # for markdown
]

templates_path = ["_templates"]
html_sidebars = {
    "**": [
        "_templates/versions.html",
    ],
}

# sphinx-notfound-page
notfound_context = {
    "title": "Page Not Found",
    "body": """
<h1>Page Not Found</h1>

<p>Sorry, we couldn't find that page.</p>

<p>Try using the search box or go to the homepage.</p>
""",
}
notfound_urls_prefix = "/pathfinding3D/"

# source suffix
source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"
language = "en"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_logo = "../assets/logo.png"
html_favicon = "../assets/favicon.ico"
html_title = "pathfinding3d"
html_show_sourcelink = False
html_show_sphinx = False
html_copy_source = False
html_show_copyright = True
html_use_index = True
# html
html_theme_options = {
    "canonical_url": "",
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "style_nav_header_background": "white",
    # Toc options
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# generate autosummary even if no references
autosummary_generate = True
autosummary_imported_members = True

# autodoc
autodoc_mock_imports = []
autodoc_typehints = "description"
autodoc_inherit_docstrings = True
autodoc_preserve_defaults = True
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "private-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
    "inherited-members": True,
    "ignore-module-all": True,
}

# coverage
coverage_show_missing_items = True
coverage_skip_undoc_in_source = True

# syntax highlighting
pygments_style = "sphinx"
highlight_language = "python3"

# napoleon
napoleon_numpy_docstring = True

# todo-section
todo_include_todos = False

# inheritance diagrams
# smaller diagrams with rectangular nodes
inheritance_graph_attrs = {
    "rankdir": "TB",
    "size": '"6.0, 8.0"',
    "fontsize": 12,
    "ratio": "compress",
    "bgcolor": "transparent",
}

inheritance_node_attrs = {
    "shape": "rect",
    "fontsize": 12,
    "color": "orange",
    "style": "filled",
    "fillcolor": "white",
}

inheritance_edge_attrs = {
    "arrowsize": 0.5,
    "penwidth": 1.0,
    "color": "orange",
}

# graphviz
graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gbgcolor=transparent",
    "-Nfontname=Helvetica",
    "-Efontname=Helvetica",
    "-Gfontname=Helvetica",
    "-Gfontsize=12",
    "-Nfontsize=12",
    "-Efontsize=12",
]

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "pathfinding3d-doc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements: dict = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files.
latex_documents = [
    (master_doc, "pathfinding3d.tex", "pathfinding3d Documentation", "pathfinding3d Contributors", "manual"),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "pathfinding3d", "pathfinding3d Documentation", [author], 1)]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files.
texinfo_documents = [
    (
        master_doc,
        "pathfinding3d",
        "pathfinding3d Documentation",
        author,
        "pathfinding3d",
        "One line description of project.",
        "Miscellaneous",
    ),
]
