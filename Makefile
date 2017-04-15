PACKAGE_NAME = classical


build_doc:
	rm -rf docs/apidoc
	sphinx-apidoc --no-toc --separate -o docs/apidoc ${PACKAGE_NAME}
	cd docs; make html


doc: build_doc
	xdg-open docs/_build/html/index.html


test:
	py.test --cov=${PACKAGE_NAME} tests


build:
	python setup.py sdist upload
