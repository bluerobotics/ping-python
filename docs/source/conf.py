# -*- coding: utf-8 -*-
import os
import sys
import logging
from datetime import date

# Global variables
root_path = os.path.abspath(os.path.join("..", ".."))

sys.path.insert(0, root_path)


SITE_URL = "https://docs.bluerobotics.com/ping-python/"
REPO_URL = "https://github.com/bluerobotics/ping-python/"
REPO_NAME = "ping-python"
PROJECT_NAME ="ping-python"

# Project information
project = PROJECT_NAME
copyright = f"{date.today().year} - Blue Robotics Inc"
author = "Blue Robotics contributors"

# General configuration
extensions = [
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinx_blue_robotics_theme",
    "sphinx_blue_robotics_theme.extensions.extras",
    "sphinx_blue_robotics_theme.extensions.cpp",
    "breathe",
    "exhale",
]
master_doc = "index"
source_suffix = {'.rst': 'restructuredtext', '.md': 'restructuredtext'}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "python_api/library_root.rst"]

# Syntax highlighting
pygments_style = "sphinx"

# Substitutions
myst_substitutions = {
  "project_name": "Blue Robotics"
}

# External links
extlinks = {
    'issue': (REPO_URL + '/issues/%s', 'issue %s')
}

# HTML output configuration
html_theme = "sphinx_blue_robotics_theme"
html_static_path = ["_static"]
html_css_files = ['custom.css']

html_theme_options = {
    "site_url": SITE_URL,
    "repo_url": REPO_URL,
    "repo_name": REPO_NAME,
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
    },
    "globaltoc_collapse": False,
    "edit_uri": "blob/master/docs/source",
        "features": [
        "navigation.sections",
        "navigation.megamenu",
        "navigation.top",
        "toc.follow",
        "toc.sticky",
        "content.tabs.link",
        "announce.dismiss",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "toggle": {
                "icon": "octicons/moon-16",
                "name": "Switch to dark mode",
            }
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "toggle": {
                "icon": "octicons/sun-16",
                "name": "Switch to light mode",
            }
        },
    ],
    "toc_title_is_page_title": True,
}

html_last_updated_fmt = "%d %b %Y"
htmlhelp_basename = "BlueRoboticsDocumentationdoc"
html_baseurl = SITE_URL
html_context = {
    "homepage_url": "https://bluerobotics.com",
    "project_url": html_baseurl, 
    "project": project, 
    "exclude_comments": True
}

# Breathe and Exhale configuration
breathe_projects = {project: os.path.join(root_path, "doc", "xml")}
breathe_default_project = project
breathe_domain_by_extension = {"h": "cpp", "py": "py"}

# Silence doxygen warnings 
suppress_warnings = [
    "ref.duplicate",  # Suppress warnings about duplicate references
    "app.add_directive",  # Suppress warnings about directives
    "autodoc.duplicate_object_description",  # Suppress warnings about duplicate object descriptions
]

exhale_args = {
    "containmentFolder":     "./python_api",
    "rootFileName":          "library_root.rst",
    "doxygenStripFromPath":  root_path,
    "rootFileTitle":         "API Reference",
    "createTreeView":        False,
    "contentsDirectives":    False,
    "exhaleExecutesDoxygen": True,
    "fullToctreeMaxDepth": 1,
    "exhaleDoxygenStdin":    f"INPUT = {os.path.join(root_path, 'brping')}",
    "verboseBuild":          True,
}

# Myst Parser options
myst_enable_extensions = ["substitution", "colon_fence"]

def setup(app):
    # Suppress Breathe duplicate object & parameter mismatch warnings
    logger = logging.getLogger("sphinx")
    logger.addFilter(lambda record: "duplicate object description" not in record.getMessage())
    logger.addFilter(lambda record: "does not match any of the parameters" not in record.getMessage())