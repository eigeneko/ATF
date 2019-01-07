'''
================================================================
format outputfile of FreeEnCal 3.2.2
================================================================
tool for compare the output of FreeEnCal_3.0 with FreeEnCal 3.2.2
file_new is for 3.2
file_old is for 3.0
Compare the AllPool and NewPool part of two outputFiles
Notice that InferenceRule And Degree are the same as InputFile. No need to compare
and the LoopNumebr part is only in 3.2. So discard also.
----------------------------------------------------------------
AllPool 10
AllPool 10
There may be invisible blank after numbers.
If not strip it, using diff command without -b will report different.
Even if they looks the same.
'''

import argparse
import subprocess
import os


# ground truth results
root_30 = 'Logic_Fragments_3.0'
# Generate from 3.2 using inputfile of 3.0
# root_32 = 'Logic_Fragments_3.2'
# Generate from 3.2 from scratch
root_32 = 'Logic_Fragments_3.2_scratch'


def fileFormat(name, path, outdir, version):

    print("Formating {}".format(name))

    fileout = os.path.join(outdir, 'clean_' + name)
    out = open(fileout, 'wt')
    with open(path, 'rt') as f:

        # del comments at first 3 rows
        if version == '3.2.2':
            for i in range(3):
                f.readline()

        for line in f:

            fragment = line.split()[0]

            # Begin of AllPool part
            # using strip to remove blanks after All Pool
            if fragment == "AllPool":
                out.write(line.strip()+'\n')

            # Begin of NewPool part
            elif fragment == "NewPool":
                out.write(line.strip()+'\n')

            # Begin of InferenceRule part, exit
            elif fragment == "InferenceRule":
                break
                
            else:
                out.write(fragment+'\n')
        out.close()
    return fileout


parser = argparse.ArgumentParser(description='FreeEnCal Outfile Compare')

parser.add_argument(dest='task', metavar='task', nargs=1, help='Input the name of logic fragments you want to compare')
args = parser.parse_args()
logicFrag = args.task[0]

if logicFrag.startswith('EcQ') or logicFrag.startswith('EenQ') or logicFrag.startswith('EeQ'):
    root_30 = os.path.join(root_30, 'predicatelogic')
    root_32 = os.path.join(root_32, 'predicatelogic')
else:
    root_30 = os.path.join(root_30, 'propositionallogic')
    root_32 = os.path.join(root_32, 'propositionallogic')

new_dir = os.path.join(root_32, logicFrag)
old_dir = os.path.join(root_30, logicFrag)
files_new = [name for name in os.listdir(new_dir) if name.startswith(logicFrag)]
files_old = [name for name in os.listdir(old_dir) if name.startswith('result')]
files_new.sort()
files_old.sort()
num_news  = len(files_new)
num_olds  = len(files_old)
print("Now compare task : {}".format(logicFrag))
print("Num of outfiles by FreeEnCal 3.2.2 : {}".format(num_news))
print("Num of outfiles by FreeEnCal 3.0.0 : {}".format(num_olds))
print(files_new)
print(files_old)
if num_news != num_olds:
    print("the number of outfiles not equal!")
else:
    for file1, file2 in zip(files_new, files_old):

        # format two files
        file_new = os.path.join(new_dir, file1)
        file_old = os.path.join(old_dir, file2)
        outdir = logicFrag+'_cmp'
        if os.path.isdir(outdir):
            pass
        else:
            os.mkdir(outdir)
        outfile1 = fileFormat(file1, file_new, outdir, '3.2.2')
        outfile2 = fileFormat(file2, file_old, outdir, '3.0')
        # Using diff to compare
        # try:
        outBytes = subprocess.check_output(' '.join(['diff', outfile1, outfile2]), shell=True)
        cmpResults = outBytes.decode('utf-8').splitlines()
        # except subprocess.CalledProcessError as e:
            # out_bytes = e.output       # Output generated before error
            # code      = e.returncode   # Return code
        if not cmpResults:
            print("OK")
            log = "No differences detected"
        with open(os.path.join(outdir, 'Log'), 'wt') as f:
            f.write(log)
        print('-'*30)
        


# parser.add_argument('-n', '--name', metavar='filename', nargs='*',
#                     dest='filenames', help='1st is file for 3.2, 2nd is file for 3.0')
# args = parser.parse_args()
# file_new = args.filenames[0]
# file_old = args.filenames[1]


# fileFormat(file_new, '3.2.2')
# fileFormat(file_old, '3.0')



   