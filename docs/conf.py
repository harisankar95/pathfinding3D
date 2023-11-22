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
copyright = "2023, Harisankar Babu"
author = "Harisankar Babu"
release = __version__
version = __version__


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.ifconfig",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    "sphinx_copybutton",
    "sphinx-prompt",
    "notfound.extension",
    "versionwarning.extension",
]

templates_path = ["_templates"]
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"
language = "en"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

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
    "inherited-members": False,
}

# coverage
coverage_show_missing_items = True
coverage_skip_undoc_in_source = True

# syntax highlighting
pygments_style = "sphinx"
highlight_language = "python3"

# html
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
    "display_version": True,
}


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
