python make_one_ma_input.py
hex2maffttext ma0.hex > ma0.ASCII
mafft --text --clustalout ma0.ASCII > outma0.ASCII
maffttext2hex outma0.ASCII > outma0.hex

