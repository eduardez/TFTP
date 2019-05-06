#!/usr/bin/make -f
# -*- mode:makefile -*-

SRC=$(wildcard *.py)

all:   	$(SRC:.py=.rtf)

%.rtf %.html: %.py
	highlight --style edit-emacs -o $@ -i $<

print:
	for i in `ls *.py`; do \
	   a2ps $$i; \
	done

clean:
	$(RM) *~ *.pyc $(SRC:.py=.html) *.rtf
