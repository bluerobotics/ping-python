# Global variables
# These can be overridden from the command line.
POETRY        = poetry
SPHINXOPTS    = -j auto
SPHINXBUILD   = $(POETRY) run sphinx-build
PAPER         =
BUILDDIR      = _build
SOURCEDIR     = source
ROOT_DIR 	  = ..

# Internal variables
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(SOURCEDIR)
AUTOBUILDOPTS   = --ignore "source/python_api/*" --ignore "source/cpp_api/*" --ignore "source/lua_api/*"
TESTSPHINXOPTS  = $(ALLSPHINXOPTS) -W --keep-going

.PHONY: all
all: dirhtml

# Setup commands
.PHONY: setupenv
setupenv:
	pip install -q poetry

.PHONY: setup
setup:
	$(POETRY) install --all-extras
	cd $(ROOT_DIR) && git submodule update --init
	$(POETRY) run python $(ROOT_DIR)/generate/generate-python.py --output-dir=$(ROOT_DIR)/brping

.PHONY: update
update:
	$(POETRY) update

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/*

# Output generation commands
dirhtml: setup
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

.PHONY: singlehtml
singlehtml: setup
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

.PHONY: preview
preview: setup
	$(POETRY) run sphinx-autobuild -b dirhtml $(ALLSPHINXOPTS) $(AUTOBUILDOPTS) $(BUILDDIR)/dirhtml --port 5500

# Testing commands
.PHONY: test
test: setup
	$(SPHINXBUILD) -b dirhtml $(TESTSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

.PHONY: linkcheck
linkcheck: setup
	$(SPHINXBUILD) -b linkcheck $(SOURCEDIR) $(BUILDDIR)/linkcheck
