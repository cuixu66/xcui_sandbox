OUT = out/
BASE = slides
SRC = $(BASE).tex
PDF = $(OUT)$(BASE).pdf

TEX = pdflatex -interaction=nonstopmode -output-directory out/
G = gvfs-open $(PDF)

$(PDF) : $(SRC)
	$(TEX) $(SRC)
	$(G)

.PHONY: clean
clean :
	rm -rf out/*
