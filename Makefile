all:
	make clean

install:
	pip install sklearn
	pip install ibm_watson
	pip install anytree
	pip install graphviz

test:
	make install
	python3 src/driver.py dataset src/input.csv src/output.csv

dataset:
	make install
	python3 src/driver.py dataset src/pruned_tweets.csv src/output.csv

classify:
	make install
	python3 src/driver.py tree src/output.csv src/tree

cross_validate:
	make install
	python3 src/driver.py cross_validate 5 src/output.csv resources/max_depth.png resources/min_samples.png

paper:
	cd doc && $(MAKE)

clean:
	rm -rf __pycache__ || true
	(rm *.log *.aux *.out *.pdf 2> /dev/null) || true
	rm src/tree* || true

