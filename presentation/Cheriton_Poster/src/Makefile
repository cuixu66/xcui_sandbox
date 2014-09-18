TEX=microfuge_poster
OUT=out
CMD=pdflatex -aux-directory=$(OUT) -output-directory=$(OUT)
all:
	mkdir -p $(OUT)
	$(CMD) $(TEX).tex
	# You can use environment variable TEXMFOUTPUT to specify output directory for bibtex files.
	# so bibtex will output everything to $(OUT) dir
	TEXMFOUTPUT=$(OUT) bibtex $(OUT)/$(TEX)
	$(CMD) $(TEX).tex
	$(CMD) $(TEX).tex


clean:
	rm -rf out/
