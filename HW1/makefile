PYTHON = python3

build:
	echo "Python does not require compiling."

run:
	${PYTHON} main.py -i ./text.fa -o patt.fa -a BF
	${PYTHON} main.py -i ./text.fa -o patt.fa -a KMP
	${PYTHON} main.py -i ./text.fa -o patt.fa -a BM
	${PYTHON} main.py -i ./text.fa -o patt.fa -a A

clean:
	rm -rf .pyc/