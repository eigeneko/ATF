'''
================================================================
format outputfile of FreeEnCal 3.2.2
================================================================
tool for compare the output of FreeEnCal_3.0 with FreeEnCal 3.2.2
file_new is for 3.2
file_old is for 3.0
Compare the AllPool and NewPool part of two outputFiles.
Notice that InferenceRule And Degree are the same as InputFile, No need to compare.
The LoopNumebr part is different
3.2: LoopNumber + number
3.0: number(only)
----------------------------------------------------------------
AllPool 10
AllPool 10
There may be invisible blank after numbers.
If not strip it, using diff command without -b will report different.
Even if they looks the same.
'''

import argparse
import subprocess
import shutil
import os
import sys

# ground truth results
root_30 = 'NBG3.0'
# Generate from 3.2 using inputfile of 3.0
root_32 = 'NBG3.2'
# Generate from 3.2 from scratch

outRoot = '/home/eigeneko'

def fileFormat(name, path, outdir, version):

    print("Formating {}".format(name))

    fileout = os.path.join(outdir, name)
    out = open(fileout, 'wt')
    with open(path, 'rt') as f:

        # del comments at first 3 rows
        if version == '3.2.2':
            f.readline()
            # numPremises = f.readline().split()[1]
            # print(numPremises)
            # for i in range(int(numPremises)):
            #     f.readline() # cancel the premises

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

root_30 = os.path.join(root_30, logicFrag)
root_32 = os.path.join(root_32, logicFrag)
outDir = os.path.join(outRoot, logicFrag+'_cmp')

if os.path.isdir(outDir):
    print("Dir already exist")
    # remove the whole dir
    shutil.rmtree(outDir)
os.mkdir(outDir)

fragments = [e for e in os.listdir(root_30) if os.path.isdir(e) and not e.startswith('.')]
fragments.sort()

print("Now handling {} Total:{}".format(logicFrag, len(fragments)))

for posi, frag in enumerate(fragments):

    new_dir = os.path.join(root_32, frag)
    old_dir = os.path.join(root_30, frag)
    files_new = [name for name in os.listdir(new_dir) if name.startswith(frag)]
    files_old = [name for name in os.listdir(old_dir) if name.startswith('result')]
    files_new.sort()
    files_old.sort()
    num_news  = len(files_new)
    num_olds  = len(files_old)
    print("="*40)
    print("No.{} Now compare task : {}".format(posi+1, frag))
    print("="*40)
    print("Num of outfiles by FreeEnCal 3.2.2 : {}".format(num_news))
    print("Num of outfiles by FreeEnCal 3.0.0 : {}".format(num_olds))


    errors = []
    if num_news != num_olds:
        print("the number of outfiles not equal!")
    else:
        for file1, file2 in zip(files_new, files_old):

            print('-'*40)
            # format two files
            file_new = os.path.join(new_dir, file1)
            file_old = os.path.join(old_dir, file2)
            outputPath = os.path.join(outDir, frag)
            if os.path.isdir(outputPath):
                pass
            else:
                os.mkdir(outputPath)
            outfile1 = fileFormat(file1, file_new, outputPath, '3.2.2')
            outfile2 = fileFormat(file2, file_old, outputPath, '3.0')
            sortfile1 = os.path.join(outputPath, 'sort_'+file1)
            sortfile2 = os.path.join(outputPath, 'sort_'+file2)

            # Using diff to compare
            try:
                p1 = subprocess.Popen(' '.join(['sort', outfile1, '>', sortfile1]), shell=True)
                p2 = subprocess.Popen(' '.join(['sort', outfile2, '>', sortfile2]), shell=True)
                p1.wait()
                p2.wait() # must wait, otherwise, diff will execute before file have been writen.
                outBytes = subprocess.check_output(' '.join(['diff', sortfile1, sortfile2]), shell=True)
                cmpResults = outBytes.decode('utf-8').splitlines()
                if not cmpResults:
                    log = "No differences detected"
                else:
                    errors.append(frag)
                with open(os.path.join(outputPath, 'Log'), 'wt') as f:
                    f.write(log)
            except subprocess.CalledProcessError as e:
                print('{} {}'.format(e.cmd, e.returncode))
                # for line in e.output.decode('utf-8').splitlines():
                    # print(line)
                # sys.exit(1)
    
if not errors:
    print(errors)
    print("All fragments are the same, no differences.")
           
            


   