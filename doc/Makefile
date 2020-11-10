all:
	make paper
	make clean

paper:
	pdflatex paper.tex 
	open paper.pdf

clean:
	(rm *.log *.aux *.out 2> /dev/null) || true
	rm -rf __pycache__ || true

