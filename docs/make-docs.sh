rm -rf _build

export SPHINXBUILD=sphinx-build
export SOURCEDIR=.
export BUILDDIR=_build

sphinx-apidoc -H "CodeReef Client package" -f -T -o package ../codereef

${SPHINXBUILD} -M $1 ${SOURCEDIR} ${BUILDDIR} ${SPHINXOPTS}
