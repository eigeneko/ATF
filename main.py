import argparse
from utils import compare, getFilePath, cleanFormula


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='FreeEnCal tools')
    parser.add_argument(dest='filenames', metavar='filenmae', nargs='*')

    parser.add_argument('-c', '--compare', metavar='file', dest='compare', nargs=2,
                    help='use diff compare two outfiles')

    parser.add_argument('-x', '--clean', metavar='file', dest='clean', action='store',
                    help='clean a FreeEnCal outfile')
    args = parser.parse_args()

    if args.compare:
        compare(args.compare[0], args.compare[1])
    elif args.clean:
        cleanFormula(args.clean)