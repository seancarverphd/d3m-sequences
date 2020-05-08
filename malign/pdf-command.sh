# ./command.sh
python make_one_ma_input.py
python parse_output.py
enscript --landscape -B -v -e@ outma0.txt -o - | ps2pdf - outma0.pdf
python list_primitive.py
enscript -B -v -e@ primitive_list.txt -o - | ps2pdf - primitive_list.pdf
