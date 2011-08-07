.PHONY: all clean

all: alphabet.svg

clean:
	rm alphabet.svg

alphabet.svg: alphabet.a
	./svgcompile.py alphabet.a alphabet.svg
