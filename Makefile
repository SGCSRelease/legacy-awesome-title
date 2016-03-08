PACKAGE=AwesomeTitleServer
RUNNER=$(PACKAGE)Runner
VERSION=$(shell git describe --tags)
OUTPUT_NAME=$(PACKAGE)-$(VERSION)

pex: $(PACKAGE)-$(VERSION).pex

dist/$(PACKAGE)-$(VERSION).tar.gz: setup.py requirements.txt
	python setup.py sdist
	pip install --upgrade pip wheel pex
	pip download -r requirements.txt -d dist/

dist/$(RUNNER)-$(VERSION).tar.gz:
	make -C .$(RUNNER)
	ln .$(RUNNER)/dist/$(RUNNER)-$(VERSION).tar.gz dist/

$(PACKAGE)-$(VERSION).pex: dist/$(PACKAGE)-$(VERSION).tar.gz dist/$(RUNNER)-$(VERSION).tar.gz requirements.txt
	pex -o $(PACKAGE)-$(VERSION).pex   --no-pypi -f dist/   -m $(RUNNER):app    -r requirements.txt   $(PACKAGE)  $(RUNNER)

clean:
	rm -rf *.egg-info  build/  dist/  $(PACKAGE)-$(VERSION).pex  */__pycache__/  ~/.pex/build/
	make -C .$(RUNNER) clean
