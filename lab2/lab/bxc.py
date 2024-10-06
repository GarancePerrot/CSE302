#! /usr/bin/env python3

# --------------------------------------------------------------------
# Requires Python3 >= 3.10

# --------------------------------------------------------------------
import argparse
import json
import os
import subprocess as sp
import sys

from bxlib.bxast         import *
from bxlib.parser        import Parser
from bxlib.bxmm          import MM
from bxlib.syntaxchecker import SynChecker
from bxlib.tac2x64     import AsmGen

# ====================================================================
# Parse command line arguments

def parse_args():
    parser = argparse.ArgumentParser(prog = os.path.basename(sys.argv[0]))

    parser.add_argument('input' , help = 'input file (.bx)')
    parser.add_argument('output', help = 'output file (.tac.json)')

    return parser.parse_args()

# ====================================================================
# Main entry point

def _main():
    args = parse_args()

    try:
        with open(args.input, 'r') as stream:
            prgm = stream.read()

    except IOError as e:
        print(f'cannot read input file {args.input}: {e}')
        exit(1)    

    print("debug: beginning parsing")
    pars = Parser()
    prgm = pars.parse(prgm)

    if prgm is None:
        exit(1)

    syn = SynChecker()
    if not syn.check(prgm):
        exit(1)

    print("debug: parsing done, beginning mm")

    mmclass = MM()
    tac_full = mmclass.mm(prgm)              #previously for bx to json: name tac_full by aout and replace rest of code

    abk = AsmGen.get_backend('x64-linux')
    asm = abk.lower(tac_full)

    basename = os.path.splitext(args.input)[0]
    basename = os.path.basename(basename)

    try:
        with open(f'{basename}.s', 'w') as stream:
            stream.write(asm)

    except IOError as e:
        print(f'cannot write outpout file {args.output}: {e}')
        exit(1)

    sp.call(['gcc', '-c', '-o', f'{basename}.o', f'{basename}.s'])
    sp.call(['gcc', '-o', f'{basename}.exe', f'{basename}.o'])

# --------------------------------------------------------------------
if __name__ == '__main__':
    _main()


""" previously for bx to json : 

    print("debug: mm done, writing in file")

    try:
        with open(args.output, 'w') as stream:
            json.dump(aout, stream, indent = 2)
            print(file = stream) # Add a new-line

    except IOError as e:
        print(f'cannot write outpout file {args.output}: {e}')
        exit(1)

# --------------------------------------------------------------------
if __name__ == '__main__':
    _main()

    """