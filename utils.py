import os
import argparse
import subprocess
import collections
def getFilePath(description):
    '''
    A wraper for get CLI arguments.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(dest='filenames', metavar='filenames', nargs='*', help='Name of input files')
    args = parser.parse_args()
    return args.file

def parsePath(file_path):
    """ 
    split directory and file name for a given file path.
    This can be replaced by os.path.split
    """
    pathList = file_path.split('/')
    fileName = pathList[-1]
    fileDir = '/'.join(pathList[:-1])
    return fileName, fileDir

def statistic(file_path):
    """
    count the number of LP, EP in output
    """
    with open(file_path, 'rt') as f:

        for line in f:
            
            fragments = line.split()
            first     = fragments[0]
            if first in ['LogicalPremise', 'EmpiricalPremise']:
                print(line.strip())

        print('-'*40)

def compare(file1, file2):
    """
    Using diff to compare.
    """
    sortfile1 = os.path.join(os.getcwd(), 'sort1')
    sortfile2 = os.path.join(os.getcwd(), 'sort2')
    try:
        p1 = subprocess.Popen(' '.join(['sort', file1, '>', sortfile1]), shell=True)
        p2 = subprocess.Popen(' '.join(['sort', file2, '>', sortfile2]), shell=True)
        p1.wait()
        p2.wait() 
        # must wait, otherwise, diff will execute before file have been writen.

        outBytes = subprocess.check_output(' '.join(['diff', sortfile1, sortfile2]), shell=True)
        cmpResults = outBytes.decode('utf-8').splitlines()
        if not cmpResults:
            log = "No differences detected"
            print(log)
        # else:
        #     with open(os.path.join(os.getcwd(), 'Log'), 'wt') as f:
        #         f.write(log)
        os.remove(sortfile1)
        os.remove(sortfile2)
        
    except subprocess.CalledProcessError as e:
        print('{} {}'.format(e.cmd, e.returncode))
        # for line in e.output.decode('utf-8').splitlines():
            # print(line)
            # sys.exit(1)

def cleanFormula(file_path):
    """
    file_path)
    ------------------------------------------------
    clear formula in AllPool, NewPool for deducing logical fragments.
    clear formula in LogicalPremise, EmpiricalPremise for deducing
    empirical theorems.
    only preserve formula, append remove ID＋式種類＋導出経路.
    """
    
    # fileName, fileDir = parsePath(file_path)
    fileDir, fileName = os.path.split(file_path)
    outName = os.path.join(fileDir, 'clean_' + fileName)
    out = open(outName, 'wt')

    print("Formating {}".format(fileName))
    with open(file_path) as f:
        nochange = True
        for line in f:

            if line.startswith('#'):
                continue
            else:
                fragment = line.split()[0]

            # This line indicate the start of nonformula part
            if fragment in ['InferenceRule', 'Degree', 'EliminationRule']:
                nochange = True

            # This line indicate the start of formula part
            elif fragment in ['AllPool', 'NewPool', 'LogicalPremise', 'EmpiricalPremise']:
                nochange = False

            # This line is a formula
            elif nochange is False:
                out.write(fragment+'\n')
                continue

            out.write(line.strip()+'\n')
        out.close()

def deduce(filePath):
    """
    filePath: Input file for FreeEnCal
    the routine for using FreeEnCal to deduce.
    """

