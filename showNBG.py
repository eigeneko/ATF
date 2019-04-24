import os
import subprocess
import argparse
from utils import autoNBG
'''
statistical analysis NBG input file.
how many Logical Premises.
how many Empirical Premises.
etc.
'''
            
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='FreeEnCal Outfile Compare')

    parser.add_argument(dest='task', metavar='task', nargs=1, help='Input the name of logic fragments you want to compare')
    args = parser.parse_args()

    function = 'analysis.py'
    logicFrag = args.task[0]
    prefix = 'format_'

    autoNBG(scripts=function, logicalFrag=logicFrag)