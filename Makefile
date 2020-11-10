all:
	make clean

test:
	make clean

paper:
	cd doc && $(MAKE)

clean:
	rm -rf __pycache__ || true
	(rm *.log *.aux *.out *.pdf 2> /dev/null) || true

