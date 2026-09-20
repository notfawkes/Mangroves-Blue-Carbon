set -e

echo "Compiling LaTeX..."

pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex

echo "Cleaning auxiliary files..."

rm -f main.aux main.log main.out main.toc main.lof main.lot

echo "Done: main.pdf"