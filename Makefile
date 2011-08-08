SVG_COMPILER = ./svgcompile.py
SVG_OUTFILE = alphabet.svg
SVG_SOURCEFILE = alphabet.xml


.PHONY: all clean

all: $(SVG_OUTFILE)

clean:
	-rm $(SVG_OUTFILE)

$(SVG_OUTFILE): $(SVG_SOURCEFILE)
	$(SVG_COMPILER) $^ $@
