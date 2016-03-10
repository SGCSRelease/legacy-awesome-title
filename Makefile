PACKAGE=AwesomeTitleServer
VERSION=$(shell git describe --tags)
OUTPUT_NAME=$(PACKAGE)-$(VERSION)

pex: clean $(PACKAGE)-$(VERSION).pex

dist/$(PACKAGE)-$(VERSION).tar.gz: setup.py requirements.txt
	python setup.py sdist
	pip install --upgrade pip wheel pex
	pip download -r requirements.txt -d dist/

$(PACKAGE)-$(VERSION).pex: dist/$(PACKAGE)-$(VERSION).tar.gz requirements.txt
	pex -o $(PACKAGE)-$(VERSION).pex   --no-pypi -f dist/ -c minhoryang -r requirements.txt   $(PACKAGE)

clean:
	rm -rf *.egg-info  build/  dist/  $(PACKAGE)-$(VERSION).pex  */__pycache__/  ~/.pex/build/  AwesomeTitleServer/config.py
