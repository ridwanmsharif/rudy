all:
	make clean

install:
	pip install sklearn
	pip install ibm_watson
	pip install anytree
	pip install graphviz

dataset:
	make install
	python3 src/driver.py dataset src/input.csv src/output.csv

classify:
	make install
	python3 src/driver.py tree src/output.csv src/tree

test:
	make clean

paper:
	cd doc && $(MAKE)

clean:
	rm -rf __pycache__ || true
	(rm *.log *.aux *.out *.pdf 2> /dev/null) || true
	rm src/tree* || true

