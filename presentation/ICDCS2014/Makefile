FINAL = Draft_9_2
OUT = out/
BASE = slides
SRC = $(BASE).tex
PDF = $(OUT)$(FINAL).pdf

TEX = pdflatex -interaction=nonstopmode -output-directory out/
RENAME = mv --verbose $(OUT)$(BASE).pdf $(PDF)
G = gnome-open $(PDF)

$(PDF) : $(SRC)
	$(TEX) $(SRC)
	$(RENAME)
	$(G)

.PHONY: clean
clean :
	rm -rf out/*
