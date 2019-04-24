import os 
import subprocess
inRoot = '/home/eigeneko/NBG_3.0'

def getUnicodeHex(char):

    return hex(ord(char))

def autoNBG(scripts, logicalFrag, inputPrefix=False):
    '''
    For each input file of NBG, call another process to execute the scripts
    '''

    inputDir = os.path.join(inRoot, logicalFrag)
    fragments = [e for e in os.listdir(inputDir) if not e.startswith('.')]
    fragments.sort()
    for frag in fragments:

        print('Now processing {}'.format(frag))

        if inputPrefix:
            inputFile = inputPrefix + frag + '.txt'
        else:
            inputFile = frag + '.txt'
            
        inputPath = os.path.join(inputDir, frag, inputFile)

        try:
            p = subprocess.Popen(' '.join(['python3', scripts, inputPath]), shell=True)
            p.wait()
        except subprocess.CalledProcessError as e:
            print('{} {}'.format(e.cmd, e.returncode))

    print("Total: {}".format(len(fragments)))