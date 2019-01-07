import os
import subprocess
import argparse
from utils import autoNBG


            
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='FreeEnCal Outfile Compare')

    parser.add_argument(dest='task', metavar='task', nargs=1, help='Input the name of logic fragments you want to compare')
    args = parser.parse_args()

    function = 'clean.py'
    logicFrag = args.task[0]

    autoNBG(scripts=function, logicalFrag=logicFrag)