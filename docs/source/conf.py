# Configuration file for the Sphinx documentation builder.
#
# Reference documentation:
#   https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# -- Project information ------------------------------------------------------
#
project = 'Ansible Ultimate Edition'
copyright = '2022, <a href="https://training.wescale.fr/">WeScale.fr</a>'
author = 'www.wescale.fr'
release = '0.0.1'
#
# -- General configuration ----------------------------------------------------
#
extensions = [
    "myst_parser",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode"
]
templates_path = ['_templates']
exclude_patterns = []
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
#
# -- Options for EPUB output --------------------------------------------------
#
version = release
epub_theme = "basic"
epub_title = "Ansible Ultimate Edition"
epub_language = "fr"
epub_exclude_files = [
    '_static/scripts/furo.js.LICENSE.txt', 
    '_static/scripts/furo.js.map',
    '_static/styles/furo-extensions.css.map', 
    '_static/styles/furo.css.map'
]
#
# -- Options for HTML output --------------------------------------------------
#
html_theme = "furo"
html_title = "Ansible Ultimate Edition"
html_logo = "static/ansible_logo.png"
#
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
#
# -- Ansible role inline doc extraction ---------------------------------------
#
import os, sys

direnv_python_libs = os.getenv("DIRENV_PYTHON_LIBS_DIR")

try:
    if direnv_python_libs:
        sys.path.insert(0, direnv_python_libs)
    import yaml2rst
except ImportError:
    raise ImportError("yaml2rst import error")

roles_src_path = os.getenv("ANSIBLE_ROLES_PATH")
if not roles_src_path:
    roles_src_path = "../../roles"
roles_doc_path = "reference/role"

ansible_roles = []

if os.path.exists(roles_src_path):
    ansible_roles = os.listdir(roles_src_path)

for element in ansible_roles:
    if not os.path.isdir(roles_src_path + "/" + element + "/defaults"):
        continue
    os_walk = os.walk(roles_src_path + "/" + element + "/defaults")
    for path, subdirs, files in os_walk:
        for filename in files:
            if filename.startswith("."):
                continue

            defaults_file = os.path.join(path, filename)
            defaults_dir = roles_doc_path + "_" + element

            yaml2rst.convert_file(
                defaults_file,
                roles_doc_path + "_" + element + ".rst",
                strip_regex=r"\s*(:?\[{3}|\]{3})\d?$",
                yaml_strip_regex=r"^\s{66,67}#\s\]{3}\d?$",
            )
            print("Converted {0}".format(defaults_dir))
