#! /usr/bin/env python3

# --------------------------------------------------------------------
# Requires Python3 >= 3.10

# --------------------------------------------------------------------
import argparse
import os
import subprocess as sp
import sys

from bxlib.bxast        import *
from bxlib.bxerrors     import Reporter, DefaultReporter
from bxlib.bxparser     import Parser
from bxlib.bxmm         import MM
from bxlib.bxsynchecker import SynChecker
from bxlib.bxasmgen     import AsmGen

# ====================================================================
# Parse command line arguments

def parse_args():
    parser = argparse.ArgumentParser(prog = os.path.basename(sys.argv[0]))

    parser.add_argument('input', help = 'input file (.bx)')

    aout = parser.parse_args()

    if os.path.splitext(aout.input)[1].lower() != '.bx':
        parser.error('input filename must end with the .bx extension')

    return aout

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

    reporter = DefaultReporter(source = prgm)
    prgm = Parser(reporter = reporter).parse(prgm)

    if prgm is None:
        exit(1)

    if not SynChecker(reporter = reporter).check(prgm):
        exit(1)

    tac = MM.mm(prgm)
    abk = AsmGen.get_backend('x64-linux')
    asm = abk.lower(tac)

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
