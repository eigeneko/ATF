import argparse
# from predicateLogicConvert import PredicateLogicConvert

conf = 'group'

def infix2pre(file):

    stdLanguage = 'pre_' + file
    fecLanguage = 'fec_' + file
    out = open(stdLanguage, 'wt')
    with open(file, 'rt')as f:

        for line in f:
            queue = []
            stack = []
            string = line.replace(' ', '')
            string = list(string.strip())
            string.reverse()
            for pos, elem in enumerate(string):
                # print(stack)
                # print(' '.join(queue[::-1]))
                if elem == ' ':
                    print('empty')

                if elem == ')':
                    stack.append(elem)

                elif elem == '(':
                    while stack[-1] != ')':
                        e = stack.pop()
                        queue.append(e) 
                    stack.pop()

                elif elem in ['⇒', '•', '=' , '∧']:
                    stack.append(elem)
                elif elem in ['G']:
                    queue.append('G(x)')
                elif elem in ['x', 'y', 'z', 'u'] and string[pos+1] in ['∃', '∀']:
                    # treat ∃x ... as a whole part
                    continue
                elif elem in ['∃', '∀']:
                    queue.append(string[pos]+string[pos-1])
                else:
                    queue.append(elem)

            for i, char in enumerate(queue):
                if char == ']':
                    queue[i] = 'EOQ'
                    
            print(' '.join(queue[::-1]), file=out)
        out.close()

        # read symbols
        symbols = list()
        with open(conf, 'rt') as f:

            for line in f:

                x = line.split()
                if not x or line[0] in ['#', '-']:
                    continue
                symbols.append((x[0], x[1]))

        out = open(fecLanguage, 'wt')
        with open(stdLanguage, 'rt') as f:
        
            for line in f:
                wff = line.strip().split()

                print(wff)
                if line.startswith('#'):
                    out.write(line)
                    continue
                
                result = []
                for e in wff:
                    find = False
                    for symbol, string in symbols:
                        if e == symbol:
                            # print(symbol, string)
                            result.append(string) 
                            find = True
                            break
                    if find == False:
                        result.append(e)    
                
                # out.write('# '+line)
                print(','.join(result), file=out)
                                    
            
        out.close()




if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='FreeEnCal Logic Fragments Convert')

    parser.add_argument(dest='file', metavar='file', nargs=1, help='Input the name of file you want to format')
    args = parser.parse_args()
    filename = args.file[0]

    infix2pre(filename)
    # PLC = PredicateLogicConvert()
    # PLC.polishOut = 'pre_test'
    # PLC.infixOut = 'infix_test'
    # PLC.infixConvert()