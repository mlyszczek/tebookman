GITSHA = $(shell git rev-parse --short HEAD)
VERSION = 9999
DESTDIR ?= /usr/local
BINDIR = $(DESTDIR)/bin
SOURCES = $(addsuffix .py, config db util version)

all: tebookman

version.py: version.py.in
	if [ $(VERSION) = 9999 ]; then \
		sed 's/tebookman_version="9999"/tebookman_version="9999-$(GITSHA)"/' $< > $@;\
	else \
		sed 's/tebookman_version="9999"/tebookman_version="$(VERSION)"/' $< > $@ ; \
	fi

tebookman.zip: tebookman.py $(SOURCES)
	cp $< __main__.py
	zip $@ __main__.py $(filter-out $<,$^)
	rm __main__.py

tebookman: tebookman.zip
	echo '#!/usr/bin/env python3' > $@
	cat $< >> $@
	chmod +x $@

install: tebookman
	install -d $(BINDIR)
	install $^ $(BINDIR)

clean:
	rm -f tebookman
	rm -f tebookman.zip
	rm -f version.py

.PHONY: clean install
