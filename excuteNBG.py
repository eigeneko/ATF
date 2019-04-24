"""
=============================================
automatically handle NBG from given files
=============================================
"""

import argparse
import subprocess
import os
import shutil

outRoot = '/home/eigeneko'
inRoot = '/home/eigeneko/NBG_3.0'
fec = '/home/eigeneko/FreeEnCal_3.2.2/FreeEnCal'

def autoNBG(logicalFrag):
    
    inputDir = os.path.join(inRoot, logicalFrag)
    outDir   = os.path.join(outRoot, logicalFrag)
    print(inputDir)

    if os.path.isdir(outDir):
        print("Dir already exist")
        shutil.rmtree(outDir) # remove the whole dir
    os.mkdir(outDir)

    fragments = [e for e in os.listdir(inputDir) if not e.startswith('.')]
    fragments.sort()

    print("Now handling {} Total:{}".format(logicalFrag, len(fragments)))
    for frag in fragments:
        print('Now processing {}'.format(frag))
        inputPath = os.path.join(inputDir, frag, frag+'.txt')
        outputPath = os.path.join(outDir, frag)
        os.mkdir(outputPath)
        os.chdir(outputPath)
        cmd = fec + ' -s -t ' + frag + ' -f CSV ' + inputPath
        out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        errReturn = out.stderr.readlines()
        outReturn = out.stdout.readlines() 
        errFile = logicalFrag + '_err'
        outFile = logicalFrag + '_out'
        with open(outFile, 'a') as f:
            for e in outReturn:
                f.write(e.decode('utf-8'))
        with open(errFile, 'a') as f:
            for e in errReturn:
                f.write(e.decode('utf-8'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FreenCal auto execution')

    parser.add_argument(dest='task', metavar='task', nargs=1, help='input the name of logic fragments used for NBG')
    args = parser.parse_args()
    logicFrag = args.task[0]

    # autoNBG('EeQ2NBG')
    # autoNBG('EeQ3NBG')
    # autoNBG('EenQ21NBG')
    # autoNBG('EenQ31NBG')
    autoNBG(logicFrag)
    
