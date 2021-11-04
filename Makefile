PACKAGE_NAME = classical


build_apidoc:
	rm -rf docs/apidoc
	sphinx-apidoc --no-toc --separate -o docs/apidoc ${PACKAGE_NAME}


build_html:
	cd docs; make html


build_doc: build_apidoc build_html


doc: build_doc
	xdg-open docs/_build/html/index.html


test:
	PACKAGE_NAME=${PACKAGE_NAME} tox


build:
	python -m build

upload:
	python -m twine upload --repository pypi dist/*
