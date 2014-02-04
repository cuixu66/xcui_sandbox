OUT = out/
BASE = design
SRC = $(BASE).tex
PDF = $(OUT)$(BASE).pdf

TEX = pdflatex -interaction=nonstopmode -output-directory out/
G = gnome-open $(PDF)

$(PDF) : $(SRC)
	$(TEX) $(SRC)
	$(G)

.PHONY: clean
clean :
	rm -rf out/*
