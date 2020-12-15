all:
	make clean

install:
	pip install sklearn
	pip install ibm_watson
	pip install anytree
	pip install graphviz
	pip install matplotlib

user:
	echo "Lets fetch some tweets for the user\n\n\n\n"
	make fetch
	echo "Lets prune the tweets\n\n\n\n"
	make prune
	echo "Lets construct a political profile\n\n\n"
	make profile
	echo "Finally lets predict their political leaning.\n\n"
	make predict
	make clean

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
	python3 src/driver.py cross_validate 5 src/output.csv resources/max_depth.png resources/min_samples.png resources/tree_max_depth resources/tree_min_samples

paper:
	cd doc && $(MAKE)

fetch:
	python3 src/individual.py  fetch $(handle) src/individual.csv

prune:
	python3 src/individual.py prune src/individual.csv src/individual_pruned.csv

profile:
	python3 src/driver.py dataset src/individual_pruned.csv src/individual_profile.csv

predict:
	python3 src/driver.py predict src/output.csv src/tree src/individual_profile.csv

clean:
	rm -rf __pycache__ || true
	(rm *.log *.aux *.out *.pdf 2> /dev/null) || true
	rm src/tree* || true
	rm src/individual.csv || true
	rm src/individual_pruned.csv || true
	# rm src/individual_profile.csv || true
	# rm resources/tree_min_samples.pdf || true
	# rm resources/tree_min_samples || true
	# rm resources/tree_max_depth.pdf || true
	# rm resources/tree_max_depth || true
	# rm resources/max_depth.png || true
	# rm resources/min_samples.png || true
