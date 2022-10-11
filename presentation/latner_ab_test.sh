pdflatex -interaction batchmode latner_ab_test.tex
echo "PDF1 =" $?

pdflatex -interaction batchmode latner_ab_test.tex
echo "PDF1 =" $?

rm *.aux
rm *.log
rm *.nav
rm *.out
rm *.snm
rm *.toc

